import logging
from bnet import game_master_service_pb2 as proto
from . import BattleNet, Service, bind_export


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GamesApi:
	class GameUtilities(Service):
		name = "bnet.protocol.game_utilities.GameUtilities"

		def __init__(self, api: BattleNet):
			self.api = api

		def process_client_request(self):
			# method_id = 1
			pass

		def presence_channel_created(self):
			# method_id = 2
			pass

		def get_player_variables(self):
			# method_id = 3
			pass

		def get_load(self):
			# method_id = 5
			pass

		def process_server_request(self):
			# method_id = 6
			pass

		def notify_game_account_online(self):
			# method_id = 7
			pass

		def notify_game_account_offline(self):
			# method_id = 8
			pass

	class GameMaster(Service):
		name = "bnet.protocol.game_master.GameMaster"

		def __init__(self, api: BattleNet):
			self.api = api

		def join_game(self):
			# method_id = 1
			pass

		def list_factories(self):
			# method_id = 2
			pass

		def find_game(self):
			# method_id = 3
			pass

		def cancel_game_entry(self):
			# method_id = 4
			pass

		def game_ended(self):
			# method_id = 5
			pass

		def player_left(self):
			# method_id = 6
			pass

		def register_server(self):
			# method_id = 7
			pass

		def unregister_server(self):
			# method_id = 8
			pass

		def register_utilities(self):
			# method_id = 9
			pass

		def unregister_utilities(self):
			# method_id = 10
			pass

		def subscribe(self):
			# method_id = 11
			pass

		def unsubscribe(self):
			# method_id = 12
			pass

		def change_game(self):
			# method_id = 13
			pass

		def get_factory_info(self):
			# method_id = 14
			pass

		def get_game_stats(self):
			# method_id = 15
			pass

	class GameMasterSubscriber(Service):
		name = "bnet.protocol.game_master.GameMasterSubscriber"

		def __init__(self, api: BattleNet):
			self.api = api

		@bind_export(1, proto.FactoryUpdateNotification)
		def notify_factory_update(self, body):
			logger.warn("TODO: handle {%s}" % body)

	class GameFactorySubscriber(Service):
		name = "bnet.protocol.game_master.GameFactorySubscriber"

		def __init__(self, api: BattleNet):
			self.api = api

		@bind_export(1, proto.GameFoundNotification)
		def notify_game_found(self, body):
			logger.warn("TODO: handle {%s}" % body)

	def __init__(self, api: BattleNet):
		self.game_utility_service = GamesApi.GameUtilities(api)
		self.game_master_service = GamesApi.GameMaster(api)
		self.game_master_subscriber_service = GamesApi.GameMasterSubscriber(api)
		self.game_factory_subscriber_service = GamesApi.GameFactorySubscriber(api)
