from rest_framework import permissions
from .models import Conversation, Message

class IsConversationParticipant(permissions.BasePermission):
    """
    Allow access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj can be Conversation or Message (we handle both)
        user = request.user
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=user.user_id).exists()
        if isinstance(obj, Message):
            # allow if user is the sender or participant of the conversation
            if obj.sender == user:
                return True
            return obj.conversation.participants.filter(user_id=user.user_id).exists()
        return False

class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Allow message creation by sender who must be a participant.
    For object-level checks, allow sender or conversation participant.
    """

    def has_permission(self, request, view):
        # for POST create: ensure sender_id in payload matches request.user (or request.user is authenticated)
        if view.action == 'create' or request.method == 'POST':
            # If token based, prefer request.user identity; optionally validate sender_id payload
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        # obj is Message instance
        user = request.user
        if obj.sender == user:
            return True
        return obj.conversation.participants.filter(user_id=user.user_id).exists()
