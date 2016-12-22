import fnvhash
import itertools
import logging
import socket
import ssl
import struct
from io import BytesIO
from bnet.rpc_pb2 import Header


logging.basicConfig(level=logging.INFO, format="[%(levelname)10s: %(filename)25s - %(funcName)25s() ] %(message)s")
logger = logging.getLogger(__name__)

user_agent = (
	"Hearthstone/4.2.12051 (PC;Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz (32629 MB);"
	"Desktop;c1385421d7a109d53e0096dfe0e0141e8b233a91;5058;NVIDIA GeForce GTX 970;"
	"NVIDIA;4318;Direct3D 9.0c [nvd3dum.dll 10.18.13.5850];3072;30;Full;"
	"Windows 8.1  (6.3.0) 64bit;8;Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz;4;True;"
	"False;False;False;True;False;False;True;True;True;False;1;False;32629;True;False;"
	"True;False;2560;1440;96;Desktop;True) Battle.net/CSharp"
)

_bindings = {}


def bind_export(method_id, protobuf):
	def binding_decorator(method):
		def binding(self, body):
			proto = protobuf()
			proto.ParseFromString(body)
			return method(self, proto)
		logger.debug("Binding method %s", method)
		method_class, method_name = method.__qualname__.rsplit(".", 1)
		_bindings[(method_class, method_id)] = (method_name, binding)
		return binding
	return binding_decorator


class Service:
	id = 255

	@property
	def hash(self):
		return fnvhash.fnv1a_32(bytes(self.name, "ascii"))

	def get_method(self, method_id):
		binding = _bindings.get((self.__class__.__qualname__, method_id))
		if not binding:
			raise ValueError("Could not find bound method for %s[%d]" % (self.name, method_id))

		def func(body):
			return binding[1](self, body)
		return func

	def get_method_name(self, method_id):
		binding = _bindings.get((self.__class__.__qualname__, method_id))
		if not binding:
			raise ValueError("Could not find bound method for %s[%d]" % (self.name, method_id))
		return binding[0]


class BattleNet:
	def __init__(self, challenge_handler):
		self.connection_api = connection_api.ConnectionApi(self)
		self.authentication_api = authentication_api.AuthenticationApi(self, challenge_handler)
		self.games_api = games_api.GamesApi(self)
		self.notification_api = notification_api.NotificationApi(self)
		self.presence_api = presence_api.PresenceApi(self)
		self.channel_api = channel_api.ChannelApi(self)
		self.friends_api = friends_api.FriendsApi(self)
		self.challenge_api = challenge_api.ChallengeApi(self)
		self.account_api = account_api.AccountApi(self)
		self.resources_api = resources_api.ResourcesApi(self)

		self.connection_api.connection_service.export_services([
			self.authentication_api.auth_client_service,
			self.games_api.game_master_subscriber_service,
			self.games_api.game_factory_subscriber_service,
			self.notification_api.notification_listener_service,
			self.channel_api.channel_subscriber_service,
			self.channel_api.channel_invitation_notify_service,
			self.friends_api.friends_notify_service,
			self.challenge_api.challenge_notify_service,
			self.account_api.account_notify_service
		])
		self.connection_api.connection_service.import_services([
			self.authentication_api.authentication_server,
			self.games_api.game_utility_service,
			self.games_api.game_master_service,
			self.notification_api.notification_service,
			self.presence_api.presence_service,
			self.channel_api.channel_service,
			self.channel_api.channel_owner_service,
			self.channel_api.channel_invitation_service,
			self.friends_api.friends_service,
			self.challenge_api.challenge_service,
			self.account_api.account_service,
			self.resources_api.resources_service
		])

		self.object_id = itertools.count()
		self.waiting_for_response = {}

	def _recv(self, count):
		buf = BytesIO()
		while len(buf.getvalue()) != count:
			buf.write(self.connection.recv(count - len(buf.getvalue())))
		return buf.getvalue()

	def next_object_id(self):
		return next(self.object_id)

	def send_request(self, service_id, method_id, body, callback, object_id=0, decode_response_as=None):
		header = Header()
		header.service_id = service_id
		header.method_id = method_id
		if object_id:
			header.object_id = object_id
		message = body.SerializeToString()
		header.size = len(message)

		if not callback:
			callback = lambda x: None

		token = len(self.waiting_for_response)
		header.token = token
		self.waiting_for_response[token] = (callback, decode_response_as)

		logger.info("Sending request for %d.%d, token=%d" % (service_id, method_id, token))
		logger.debug("Sending request. Header: {%s}" % header)

		header_buf = header.SerializeToString()
		self.connection.send(struct.pack(">H", len(header_buf)))
		self.connection.send(header_buf)
		self.connection.send(message)

	def connect(self, address, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection = ssl.wrap_socket(sock)
		self.connection.connect((address, port))

		self.connection_api.connection_service.connect()

	def handle_packets(self):
		header_size = struct.unpack(">H", self._recv(2))[0]
		header = Header()
		header.ParseFromString(self._recv(header_size))
		logger.debug("Received header: {%s}" % header)
		data = self._recv(header.size)
		if header.service_id == 254:
			assert header.method_id == 0
			if header.status:
				raise Exception("Got error %d for token=%d" % (header.status, header.token))
			if header.token in self.waiting_for_response:
				logger.info("Got response for token=%d", header.token)
				callback, proto = self.waiting_for_response[header.token]
				if proto:
					body = proto()
					body.ParseFromString(data)
				else:
					body = data
				callback(body)
				del self.waiting_for_response[header.token]
			else:
				raise Exception("Got response but no handler was waiting for it")
		else:
			service = self.connection_api.connection_service.exported_services[header.service_id]
			logger.info("Got request for %d.%d -> %s.%s" % (header.service_id, header.method_id, service.name, service.get_method_name(header.method_id)))
			response = service.get_method(header.method_id)(data)
			if response:
				logger.info("Sending response")
				message = response.SerializeToString()
				header.service_id = 254
				header.method_id = 0
				header.size = len(message)
				header_buf = header.SerializeToString()
				self.connection.send(struct.pack(">H", len(header_buf)))
				self.connection.send(header_buf)
				self.connection.send(message)

	def on_select_game_account(self, nodata):
		self.friends_api.friends_service.subscribe_to_friends()
		logger.info("Game account selected")


# Import at the end to avoid a cyclic import
from . import (
	account_api, authentication_api, challenge_api, channel_api, connection_api,
	friends_api, games_api, notification_api, presence_api, resources_api
)
