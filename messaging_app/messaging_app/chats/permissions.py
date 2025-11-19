from rest_framework import permissions
from .models import Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only participants of a conversation can send/view/update/delete messages.
    """

    def has_permission(self, request, view):
        # السماح فقط للمستخدمين المصادق عليهم
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # التحقق من أن المستخدم مشارك في المحادثة
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.conversation.participants.all()

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()

        return request.user in obj.conversation.participants.all()
