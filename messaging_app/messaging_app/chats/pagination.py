# chats/pagination.py

from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    فئة ترقيم مخصصة لتقسيم قائمة الرسائل.
    تحدد حجم الصفحة الثابت بـ 20 رسالة.
    """
    # تحديد حجم الصفحة الإجباري (20 رسالة)
    page_size = 20
    # السماح بتغيير حجم الصفحة عبر البارامتر 'page_size' في طلب الـ API
    page_size_query_param = 'page_size' 
    # تحديد الحد الأقصى لحجم الصفحة الذي يمكن للمستخدم طلبه
    max_page_size = 100