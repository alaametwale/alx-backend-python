import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.NumberFilter(field_name="sender__id")
    receiver = django_filters.NumberFilter(field_name="receiver__id")
    start_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'start_date', 'end_date']
