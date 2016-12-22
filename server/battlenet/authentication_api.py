import logging
import sys
from bnet import authentication_service_pb2 as proto
from bnet.account_types_pb2 import AccountId
from bnet.entity_pb2 import EntityId
from bnet.rpc_pb2 import NoData
from . import BattleNet, Service, bind_export, user_agent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthenticationApi:
	class AuthenticationServer(Service):
		name = "bnet.protocol.authentication.AuthenticationServer"

		def __init__(self, api: BattleNet, challenge_handler):
			self.api = api
			self.challenge_handler = challenge_handler
			self._failed_count = -1

		def logon(self):
			p = proto.LogonRequest()
			p.program = "WTCG"
			p.platform = "Win"
			p.locale = "enUS"
			# p.email = None
			p.version = "12051"
			p.application_version = 1
			p.public_computer = False
			# p.sso_id = None
			p.disconnect_on_cookie_fail = False
			p.allow_logon_queue_notifications = True
			p.web_client_verification = True
			# p.cached_web_credentials = None
			p.user_agent = user_agent

			self.api.send_request(self.id, 1, p, None)

		def module_notify(self):
			# method_id = 2
			pass

		def module_message(self):
			# method_id = 3
			pass

		def select_game_account_DEPRECATED(self, game_account):
			p = EntityId()
			p.low = game_account.low
			p.high = game_account.high

			self.api.send_request(self.id, 4, p, self.api.on_select_game_account)

		def generate_temp_cookie(self):
			# method_id = 5
			pass

		def select_game_account(self):
			# method_id = 6
			pass

		def verify_web_credentials(self, auth_url):
			self._failed_count += 1
			if self._failed_count > 3:
				raise Exception("Failed to login 3 times, bailing out")
			logger.info("Relieved web auth url: '%s'" % auth_url)
			verify_request = proto.VerifyWebCredentialsRequest()
			verify_request.web_credentials = self.challenge_handler(auth_url)
			self.api.send_request(self.id, 7, verify_request, None)

	class AuthenticationClient(Service):
		name = "bnet.protocol.authentication.AuthenticationClient"

		def __init__(self, api: BattleNet):
			self.api = api
			self.account_entity = None
			self.game_account = None
			self.game_accounts = []

		@bind_export(1, proto.ModuleLoadRequest)
		def module_load(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(2, proto.ModuleMessageRequest)
		def module_message(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(3, proto.AccountSettingsNotification)
		def account_settings(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(4, proto.ServerStateChangeRequest)
		def server_state_change(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(5, proto.LogonResult)
		def logon_complete(self, body):
			logger.info("Login complete for %s, selecting game account", body.battle_tag)
			self.account_entity = body.account
			self.api.presence_api.presence_service.subscribe(body.account)
			for account in body.game_account:
				self.game_accounts.append(account)
				self.api.presence_api.presence_service.subscribe(account)
			if len(self.game_accounts):
				self.game_account = self.game_accounts[0]
			self.api.authentication_api.authentication_server.select_game_account_DEPRECATED(self.game_account)

		@bind_export(6, proto.MemModuleLoadRequest)
		def mem_module_load(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(10, proto.LogonUpdateRequest)
		def logon_update(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(11, proto.VersionInfoNotification)
		def version_info_updated(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(12, proto.LogonQueueUpdateRequest)
		def logon_queue_update(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(13, NoData)
		def logon_queue_end(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(14, proto.GameAccountSelectedRequest)
		def game_account_selected(self, body):
			logger.warn("TODO: handle {%s}" % body)

	def __init__(self, api: BattleNet, challenge_handler):
		self.authentication_server = AuthenticationApi.AuthenticationServer(api, challenge_handler)
		self.auth_client_service = AuthenticationApi.AuthenticationClient(api)

