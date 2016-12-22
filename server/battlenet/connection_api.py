import logging
from bnet import connection_service_pb2 as proto
from . import BattleNet, Service, bind_export


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionApi:
	class ConnectionService(Service):
		id = 0
		name = "bnet.protocol.connection.ConnectionService"

		def __init__(self, api: BattleNet):
			self.api = api
			self._services_to_export = []
			self._services_to_import = []
			self.exported_services = {}
			self.imported_services = {}

		def export_services(self, services):
			self._services_to_export += services

		def import_services(self, services):
			self._services_to_import += services

		def connect(self):
			p = proto.ConnectRequest()
			for imported_service in self._services_to_import:
				p.bind_request.imported_service_hash.append(imported_service.hash)
			for i, exported_service in enumerate([self] + self._services_to_export):
				logger.info("Exporting service id=%d name=%s" % (i, exported_service.name))
				exported_service.id = i
				p.bind_request.exported_service.add(
					hash=exported_service.hash,
					id=exported_service.id
				)
				self.exported_services[i] = exported_service

			self.api.send_request(self.id, 1, p, self.on_connect, decode_response_as=proto.ConnectResponse)

		def on_connect(self, response):
			logger.debug("Connection response {%s}" % response)
			assert response.bind_result == 0

			for service_id, service in zip(response.bind_response.imported_service_id, self._services_to_import):
				logger.info("Importing service id=%d name=%s" % (service_id, service.name))
				service.id = service_id
				self.imported_services[service_id] = service

			self.api.authentication_api.authentication_server.logon()

		def bind(self):
			# method_id = 2
			pass

		def echo(self):
			# method_id = 3
			pass

		def force_disconnect(self):
			# method_id = 4
			pass

		def keep_alive(self):
			# method_id = 5
			pass

		def encrypt(self):
			# method_id = 6
			pass

		def request_disconnect(self):
			# method_id = 7
			pass

		@bind_export(3, proto.EchoRequest)
		def handle_echo_request(self, body):
			response = proto.EchoResponse()
			if body.time:
				response.time = body.time
			if body.payload:
				response.payload = body.payload
			return response

		@bind_export(4, proto.DisconnectNotification)
		def handle_force_disconnect_request(self, body):
			logger.fatal("Got force disconnect {%s}" % body)

	def __init__(self, api: BattleNet):
		self.connection_service = ConnectionApi.ConnectionService(api)
