from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from .filters import MessageFilter
from .permissions import IsMessageOwner
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination


class MessageListView(generics.ListAPIView):
    """
    API endpoint to return paginated + filtered messages.
    """
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    # Enable filtering
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    # Enable pagination
    pagination_class = MessagePagination


class MessageDetailView(generics.RetrieveAPIView):
    """
    Get a single message with permission protection.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwner]
