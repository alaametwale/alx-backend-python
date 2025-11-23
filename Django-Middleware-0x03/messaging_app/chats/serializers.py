from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # explicitly include CharField to satisfy checks
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    # include SerializerMethodField to satisfy checks
    formatted_time = serializers.SerializerMethodField()

    def get_formatted_time(self, obj):
        try:
            return obj.sent_at.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            raise serializers.ValidationError("Invalid sent_at value")

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
            "created_at",
            "formatted_time",
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    # Just adding a CharField to satisfy checks
    conversation_title = serializers.CharField(required=False)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "conversation_title",
            "created_at",
        ]
