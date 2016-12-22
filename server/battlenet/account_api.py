import logging
from bnet import account_service_pb2 as proto
from . import BattleNet, Service, bind_export


logger = logging.getLogger(__name__)


class AccountApi:
	class AccountService(Service):
		name = "bnet.protocol.account.AccountService"

		def __init__(self, api: BattleNet):
			self.api = api

		def get_game_account(self):
			# method_id = 12
			pass

		def get_account(self):
			# method_id = 13
			pass

		def create_game_account(self):
			# method_id = 14
			pass

		def is_igr_address(self):
			# method_id = 15
			pass

		def cache_expire(self):
			# method_id = 20
			pass

		def credential_update(self):
			# method_id = 21
			pass

		def flag_update(self):
			# method_id = 22
			pass

		def get_wallet_list(self):
			# method_id = 23
			pass

		def get_e_balance(self):
			# method_id = 24
			pass

		def subscribe(self):
			# method_id = 25
			pass

		def unsubscribe(self):
			# method_id = 26
			pass

		def get_e_balance_restrictions(self):
			# method_id = 27
			pass

		def get_account_state(self):
			# method_id = 30
			pass

		def get_game_account_state(self):
			# method_id = 31
			pass

		def get_licenses(self):
			# method_id = 32
			pass

		def get_game_time_remaining_info(self):
			# method_id = 33
			pass

		def get_game_session_info(self):
			# method_id = 34
			pass

		def get_c_a_i_s_info(self):
			# method_id = 35
			pass

		def forward_cache_expire(self):
			# method_id = 36
			pass

	class AccountNotify(Service):
		name = "bnet.protocol.account.AccountNotify"

		def __init__(self, api: BattleNet):
			self.api = api

		@bind_export(1, proto.AccountStateNotification)
		def notify_account_state_updated(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(2, proto.GameAccountStateNotification)
		def notify_game_account_state_updated(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(3, proto.GameAccountNotification)
		def notify_game_accounts_updated(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(4, proto.GameAccountSessionNotification)
		def notify_game_session_updated(self, body):
			logger.warn("TODO: handle {%s}" % body)

	def __init__(self, api: BattleNet):
		self.account_service = AccountApi.AccountService(api)
		self.account_notify_service = AccountApi.AccountNotify(api)
