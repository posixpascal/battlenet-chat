import logging
from bnet import presence_service_pb2 as proto
from . import BattleNet, Service


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PresenceApi:
	class PresenceService(Service):
		name = "bnet.protocol.presence.PresenceService"

		def __init__(self, api: BattleNet):
			self.api = api

		def subscribe(self, account):
			p = proto.SubscribeRequest()
			p.entity_id.low = account.low
			p.entity_id.high = account.high
			p.object_id = self.api.next_object_id()
			self.api.send_request(self.id, 1, p, None)

		def unsubscribe(self):
			# method_id = 2
			pass

		def update(self):
			# method_id = 3
			pass

		def query(self):
			# method_id = 4
			pass

	def __init__(self, api: BattleNet):
		self.presence_service = PresenceApi.PresenceService(api)
