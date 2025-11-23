# chats/filters.py

import django_filters
from django.db.models import Q
from .models import Message  # افترضنا أن نموذج الرسالة موجود هنا

class MessageFilter(django_filters.FilterSet):
    """
    فئة تصفية مخصصة للرسائل تسمح بالتصفية حسب:
    1. مستخدم معين (مرسل أو مستقبل).
    2. النطاق الزمني للإرسال (قبل أو بعد تاريخ ووقت معين).
    """
    # تصفية الرسائل التي تخص مستخدم معين (سواء كان مرسلاً أو مستقبلاً)
    user = django_filters.NumberFilter(
        method='filter_by_user', 
        label="Filter by messages involving a specific user ID"
    )

    # تصفية الرسائل المرسلة في أو بعد تاريخ/وقت معين
    sent_after = django_filters.DateTimeFilter(
        field_name='timestamp', 
        lookup_expr='gte',  # greater than or equal to
        label="Messages sent after (YYYY-MM-DDTHH:MM:SSZ)"
    )

    # تصفية الرسائل المرسلة في أو قبل تاريخ/وقت معين
    sent_before = django_filters.DateTimeFilter(
        field_name='timestamp', 
        lookup_expr='lte',  # less than or equal to
        label="Messages sent before (YYYY-MM-DDTHH:MM:SSZ)"
    )

    class Meta:
        model = Message
        # الحقول التي سيتم إنشاء فلاتر تلقائية لها
        fields = ['sender', 'recipient', 'timestamp'] 

    # طريقة مخصصة لتصفية الرسائل حيث يكون المستخدم هو المرسل أو المستقبل
    def filter_by_user(self, queryset, name, value):
        # استخدام Q objects لتطبيق شرط OR
        return queryset.filter(
            Q(sender_id=value) | Q(recipient_id=value)
        )