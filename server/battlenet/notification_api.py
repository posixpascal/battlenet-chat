import logging
from bnet.notification_service_pb2 import Notification
from bnet.attribute_pb2 import Variant
from . import BattleNet, Service, bind_export

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationApi:
	class NotificationService(Service):
		name = "bnet.protocol.notification.NotificationService"

		def __init__(self, api: BattleNet):
			self.api = api

		def send_notification(self, target_id, message):
			notification = Notification()
			notification.target_id.low = target_id.low
			notification.target_id.high = target_id.high
			notification.type = "WHISPER"
			value = Variant()
			value.string_value = message
			notification.attribute.add(
				name="whisper",
				value=value
			)
			self.api.send_request(self.id, 1, notification, None)

		def register_client(self):
			# method_id = 2
			pass

		def unregister_client(self):
			# method_id = 3
			pass

		def find_client(self):
			# method_id = 4
			pass

	class NotificationListener(Service):
		name = "bnet.protocol.notification.NotificationListener"

		def __init__(self, api: BattleNet):
			self.api = api
			self.whisper_listeners = []

		@bind_export(1, Notification)
		def on_notification_received(self, body):
			if body.type == "WHISPER":
				print(body)
				for callback in self.whisper_listeners:
					callback(body.sender_battle_tag, body.attribute[0].value.string_value, body.sender_id)
			else:
				logger.warn("TODO: handle non-whisper {%s}" % body)

		def add_whisper_listener(self, callback):
			self.whisper_listeners.append(callback)

	def __init__(self, api: BattleNet):
		self.notification_service = NotificationApi.NotificationService(api)
		self.notification_listener_service = NotificationApi.NotificationListener(api)

