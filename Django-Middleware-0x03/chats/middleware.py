# chats/middleware.py

import logging
from datetime import datetime

# إعداد المسجل (Logger)
# المسجل سيكتب الرسائل في ملف 'requests.log'
# يجب التأكد من أن المسار صحيح داخل بيئة المشروع
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'  # سنستخدم فقط الرسالة التي نمررها، لأننا نتحكم في التنسيق بأنفسنا
)

class RequestLoggingMiddleware:
    """
    Middleware لتسجيل طلبات المستخدمين إلى ملف 'requests.log'.
    """

    def __init__(self, get_response):
        """
        يتم استدعاء الدالة __init__ مرة واحدة عند تهيئة الخادم.
        """
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        """
        يتم استدعاء الدالة __call__ لكل طلب وارد.
        هنا يتم تنفيذ منطق التسجيل.
        """
        
        # 1. تنفيذ منطق التسجيل (Logging)
        
        # محاولة الحصول على اسم المستخدم. إذا كان المستخدم غير مسجل الدخول،
        # نستخدم "AnonymousUser" أو "Guest"
        user = getattr(request, 'user', 'Guest')
        # Django عادةً ما يضيف خاصية 'user' لـ request بعد تطبيق AuthenticationMiddleware
        user_info = str(user) if user and not user == 'Guest' and user.is_authenticated else 'Guest'
        
        # إنشاء سطر التسجيل المطلوب
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - User: {user_info} - Path: {request.path}"
        
        # كتابة الرسالة إلى ملف requests.log
        self.logger.info(log_message)