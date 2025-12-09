# chats/views.py

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer
from .pagination import MessagePagination  # استيراد فئة الترقيم المخصصة
from .filters import MessageFilter      # استيراد فئة التصفية المخصصة
# من المفترض أن تكون لديك الأذونات والسيريالايزر والنماذج الخاصة بك

class MessageViewSet(viewsets.ModelViewSet):
    # تعيين فئة الترقيم المخصصة (تطبق 20 رسالة لكل صفحة)
    pagination_class = MessagePagination 
    
    # تحديد الخلفيات (backends) المستخدمة للتصفية
    filter_backends = [DjangoFilterBackend] 
    
    # تحديد فئة التصفية التي سيتم استخدامها
    filterset_class = MessageFilter 

    serializer_class = MessageSerializer
    # permission_classes = [IsAuthenticated] # مثال على الأذونات

    # تحديد الاستعلام الأساسي (queryset) لضمان أن المستخدم يرى رسائله فقط
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # تصفية الرسائل حيث يكون المستخدم الحالي هو المرسل أو المستقبل
            return Message.objects.filter(
                Q(sender=user) | Q(recipient=user)
            ).order_by('-timestamp')
        # إذا لم يكن المستخدم مصادقًا، يمكن إرجاع استعلام فارغ أو حسب سياسة الأذونات لديك
        return Message.objects.none()