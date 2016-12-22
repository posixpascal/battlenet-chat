import logging
from bnet import friends_service_pb2 as proto
from . import BattleNet, Service, bind_export
from bnet.entity_pb2 import EntityId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FriendsApi:
	class FriendsService(Service):
		name = "bnet.protocol.friends.FriendsService"

		def __init__(self, api: BattleNet):
			self.api = api
			self.subscribe_friends_listeners = []

		def subscribe_to_friends(self):
			logger.info("Subscribing to friends")
			p = proto.SubscribeToFriendsRequest()
			p.object_id = 0
			self.api.send_request(
				self.id, 1, p,
				self.subscribe_to_friends_callback,
				decode_response_as=proto.SubscribeToFriendsResponse
			)
			self.view_friends()

		def subscribe_to_friends_callback(self, response):
			for callback in self.subscribe_friends_listeners:
					callback("{}".format(response))

		def add_subscribe_friends_listener(self, callback):
			self.subscribe_friends_listeners.append(callback)

		def send_invitation(self):
			# method_id = 2
			pass

		def accept_invitation(self):
			# method_id = 3
			pass

		def revoke_invitation(self):
			# method_id = 4
			pass

		def decline_invitation(self):
			# method_id = 5
			pass

		def ignore_invitation(self):
			# method_id = 6
			pass

		def assign_role(self):
			# method_id = 7
			pass

		def remove_friend(self):
			# method_id = 8
			pass

		def view_friends(self):
			logger.info("Subscribing to friends")
			p = proto.ViewFriendsRequest()
			entity = EntityId()
			entity.low = 120159008
			entity.high = 144115193835963207
			#self.api.send_request(
			#	self.id, 9, entity,
			#	self.view_friends_callback,
			#	decode_response_as=proto.ViewFriendsResponse
			#)
			
		def view_friends_callback(self, data):
			with open("friends.json", "w") as f:
				f.write("{}".format(data))


		def update_friend_state(self):
			# method_id = 10
			pass

		def unsubscribe_to_friends(self):
			# method_id = 11
			pass

		def revoke_all_invitations(self):
			# method_id = 12
			pass

	class FriendsNotify(Service):
		name = "bnet.protocol.friends.FriendsNotify"

		def __init__(self, api: BattleNet):
			self.api = api

		@bind_export(1, proto.FriendNotification)
		def notify_friend_added(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(2, proto.FriendNotification)
		def notify_friend_removed(self, body):
			# FIXME add listeners. body.id is EntityId
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(3, proto.InvitationNotification)
		def notify_received_invitation_added(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(4, proto.InvitationNotification)
		def notify_received_invitation_removed(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(5, proto.InvitationNotification)
		def notify_sent_invitation_added(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(6, proto.InvitationNotification)
		def notify_sent_invitation_removed(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(7, proto.UpdateFriendStateNotification)
		def notify_update_friend_state(self, body):
			logger.warn("TODO: handle {%s}" % body)

	def __init__(self, api: BattleNet):
		self.friends_service = FriendsApi.FriendsService(api)
		self.friends_notify_service = FriendsApi.FriendsNotify(api)
