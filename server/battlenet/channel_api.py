import logging
from bnet import channel_invitation_service_pb2 as invitation_proto
from bnet import channel_service_pb2 as proto
from bnet.presence_types_pb2 import ChannelState
from . import BattleNet, Service, bind_export


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChannelApi:
	class Channel(Service):
		name = "bnet.protocol.channel.Channel"

		def __init__(self, api: BattleNet):
			self.api = api

		def add_member(self):
			# method_id = 1
			pass

		def remove_member(self):
			# method_id = 2
			pass

		def send_message(self):
			# method_id = 3
			pass

		def update_channel_state(self):
			# method_id = 4
			pass

		def update_member_state(self):
			# method_id = 5
			pass

		def dissolve(self):
			# method_id = 6
			pass

		def add_member(self):
			# method_id = 7
			pass

		def unsubscribe_member(self):
			# method_id = 8
			pass

	class ChannelOwner(Service):
		name = "bnet.protocol.channel.ChannelOwner"

		def __init__(self, api: BattleNet):
			self.api = api

		def get_channel_id(self):
			# method_id = 1
			pass

		def create_channel(self):
			# method_id = 2
			pass

		def join_channel(self):
			# method_id = 3
			pass

		def find_channel(self):
			# method_id = 4
			pass

		def get_channel_info(self):
			# method_id = 5
			pass

		def subscribe_channel(self):
			# method_id = 6
			pass

	class ChannelInvitationService(Service):
		name = "bnet.protocol.channel_invitation.ChannelInvitationService"

		def __init__(self, api: BattleNet):
			self.api = api

		def subscribe(self):
			# method_id = 1
			pass

		def unsubscribe(self):
			# method_id = 2
			pass

		def send_invitation(self):
			# method_id = 3
			pass

		def accept_invitation(self):
			# method_id = 4
			pass

		def decline_invitation(self):
			# method_id = 5
			pass

		def revoke_invitation(self):
			# method_id = 6
			pass

		def suggest_invitation(self):
			# method_id = 7
			pass

		def increment_channel_count(self):
			# method_id = 8
			pass

		def decrement_channel_count(self):
			# method_id = 9
			pass

		def update_channel_count(self):
			# method_id = 10
			pass

		def list_channel_count(self):
			# method_id = 11
			pass

	class ChannelSubscriber(Service):
		name = "bnet.protocol.channel.ChannelSubscriber"

		def __init__(self, api: BattleNet):
			self.api = api

		@bind_export(1, proto.AddNotification)
		def notify_add(self, body):
			presence = body.channel_state.Extensions[ChannelState.presence]
			logger.info("Notify add for %r" % {
				str(x.field.key).replace("\n", " "): str(x.field.value).replace("\n", " ") for x in presence.field_operation
			})

		@bind_export(2, proto.JoinNotification)
		def notify_join(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(3, proto.RemoveNotification)
		def notify_remove(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(4, proto.LeaveNotification)
		def notify_leave(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(5, proto.SendMessageNotification)
		def notify_send_message(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(6, proto.UpdateChannelStateNotification)
		def notify_update_channel_state(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(7, proto.UpdateMemberStateNotification)
		def notify_update_member_state(self, body):
			logger.warn("TODO: handle {%s}" % body)

	class ChannelInvitationNotify(Service):
		name = "bnet.protocol.channel_invitation.ChannelInvitationNotify"

		def __init__(self, api: BattleNet):
			self.api = api

		@bind_export(1, invitation_proto.InvitationAddedNotification)
		def notify_received_invitation_added(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(2, invitation_proto.InvitationRemovedNotification)
		def notify_received_invitation_removed(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(3, invitation_proto.SuggestionAddedNotification)
		def notify_received_suggestion_added(self, body):
			logger.warn("TODO: handle {%s}" % body)

		@bind_export(4, invitation_proto.HasRoomForInvitationRequest)
		def has_room_for_invitation(self, body):
			logger.warn("TODO: handle {%s}" % body)

	def __init__(self, api: BattleNet):
		self.channel_service = ChannelApi.Channel(api)
		self.channel_owner_service = ChannelApi.ChannelOwner(api)
		self.channel_invitation_service = ChannelApi.ChannelInvitationService(api)
		self.channel_subscriber_service = ChannelApi.ChannelSubscriber(api)
		self.channel_invitation_notify_service = ChannelApi.ChannelInvitationNotify(api)
