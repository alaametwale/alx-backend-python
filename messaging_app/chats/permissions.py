from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update or delete messages.
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions: allow only participants
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.conversation.participants.all()
        # Write permissions: PUT, PATCH, DELETE only for participants
        if request.method in ['PUT', 'PATCH', 'DELETE', 'POST']:
            return request.user in obj.conversation.participants.all()
        return False
