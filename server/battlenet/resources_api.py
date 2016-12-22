import logging
from . import BattleNet, Service


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResourcesApi:
	class ResourcesService(Service):
		name = "bnet.protocol.resources.Resources"

		def __init__(self, api: BattleNet):
			self.api = api

		def get_content_handle(self):
			# method_id = 1
			pass

	def __init__(self, api: BattleNet):
		self.resources_service = ResourcesApi.ResourcesService(api)
