from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission: only participants of a conversation can access or modify messages.
    """

    def has_object_permission(self, request, view, obj):
        # Check if user is part of the conversation
        return request.user in obj.conversation.participants.all()

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated
