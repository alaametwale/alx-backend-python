<<<<<<< HEAD
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

=======
from rest_framework.permissions import IsAuthenticated
from .permissions import IsConversationParticipant, IsMessageSenderOrParticipant
>>>>>>> 967fb48 (Save local changes before pulling)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
<<<<<<< HEAD
    filter_backends = [filters.SearchFilter]
    search_fields = ['conversation_id']

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])

        if not participants:
            return Response({"error": "participants field is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(user_id__in=participants)

        if users.count() != len(participants):
            return Response({"error": "Invalid participant IDs"},
                            status=status.HTTP_400_BAD_REQUEST)

        conv = Conversation.objects.create()
        conv.participants.set(users)
        conv.save()

        serializer = ConversationSerializer(conv)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        sender_id = request.data.get("sender_id")
        text = request.data.get("message_body")

        if not sender_id or not text:
            return Response(
                {"error": "sender_id and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found"},
                            status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=text
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )

=======
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    # rest of class as before...
>>>>>>> 967fb48 (Save local changes before pulling)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
<<<<<<< HEAD
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_id']

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation_id")
        sender_id = request.data.get("sender_id")
        body = request.data.get("message_body")

        if not conversation_id or not sender_id or not body:
            return Response(
                {"error": "conversation_id, sender_id, message_body required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conv = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found"},
                            status=status.HTTP_404_NOT_FOUND)

        msg = Message.objects.create(
            conversation=conv,
            sender=sender,
            message_body=body
        )

        return Response(MessageSerializer(msg).data,
                        status=status.HTTP_201_CREATED)
=======
    permission_classes = [IsAuthenticated, IsMessageSenderOrParticipant]
    # rest of class as before...
>>>>>>> 967fb48 (Save local changes before pulling)
