import logging
from bnet import challenge_service_pb2 as proto
from . import BattleNet, Service, bind_export


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChallengeApi:
	class ChallengeService(Service):
		name = "bnet.protocol.challenge.ChallengeService"

		def __init__(self, api: BattleNet):
			self.api = api

		def challenge_picked(self):
			# method_id = 1
			pass

		def challenge_answered(self):
			# method_id = 2
			pass

		def challenge_cancelled(self):
			# method_id = 3
			pass

	class ChallengeNotify(Service):
		name = "bnet.protocol.challenge.ChallengeNotify"

		def __init__(self, api: BattleNet):
			self.api = api

		def __init__(self, api: BattleNet):
			self.api = api

		@bind_export(1, proto.ChallengeUserRequest)
		def challenge_user(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(2, proto.ChallengeResultRequest)
		def challenge_result(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(3, proto.ChallengeExternalRequest)
		def on_external_challenge(self, body):
			if body.payload_type != "web_auth_url":
				raise Exception("Don't know how to respond to challenge type %s" % body.payload_type)
			self.api.authentication_api.authentication_server.verify_web_credentials(body.payload)

		@bind_export(4, proto.ChallengeExternalResult)
		def on_external_challenge_result(self, body):
			logger.warn("TODO: handle {%s}" % body)

	def __init__(self, api: BattleNet):
		self.challenge_service = ChallengeApi.ChallengeService(api)
		self.challenge_notify_service = ChallengeApi.ChallengeNotify(api)
