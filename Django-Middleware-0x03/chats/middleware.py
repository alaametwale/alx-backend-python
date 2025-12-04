# Django-Middleware-0x03/chats/middleware.py

import logging
import time
from datetime import datetime, time as time_obj, timedelta

from django.http import HttpResponseForbidden

# ----------------------------------------------------------------------
# إعداد المسجل (Logger) لـ Task 1
# ----------------------------------------------------------------------
# المسجل سيكتب الرسائل في ملف 'requests.log' في مجلد المشروع الرئيسي
# يتم إعداد المسار والملف هنا
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s' 
)

class RequestLoggingMiddleware:
    """
    1. Middleware لتسجيل طلبات المستخدمين إلى ملف 'requests.log'.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        # الحصول على اسم المستخدم. 'Guest' لغير المسجلين أو عند الفشل
        user = getattr(request, 'user', 'Guest')
        user_info = str(user) if user and hasattr(user, 'is_authenticated') and user.is_authenticated else 'Guest'
        
        # إنشاء سطر التسجيل المطلوب: "{datetime.now()} - User: {user} - Path: {request.path}"
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - User: {user_info} - Path: {request.path}"
        
        self.logger.info(log_message)
        
        response = self.get_response(request)
        return response

# ----------------------------------------------------------------------
# Task 2: تقييد الوصول حسب الوقت (خارج 6 مساءً و 9 مساءً)
# ----------------------------------------------------------------------

class RestrictAccessByTimeMiddleware:
    """
    2. Middleware يقيد الوصول إلى الدردشة (الواجهة) خارج ساعات العمل المحددة:
    السماح بالوصول من 6 مساءً (18:00) إلى 9 مساءً (21:00).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # ساعات العمل المسموح بها (Inclusive)
        self.start_time = time_obj(18, 0, 0)  # 6 PM
        self.end_time = time_obj(21, 0, 0)    # 9 PM

    def __call__(self, request):
        current_time = datetime.now().time()
        
        # التحقق: إذا كان الوقت الحالي قبل 6 مساءً (18:00) أو بعد 9 مساءً (21:00)
        if not (self.start_time <= current_time <= self.end_time):
            # رفض الوصول مع إرجاع خطأ 403 Forbidden
            return HttpResponseForbidden("Access to chat is restricted outside of 6 PM and 9 PM.")

        response = self.get_response(request)
        return response

# ----------------------------------------------------------------------
# Task 3: كشف وحظر اللغة المسيئة (تحديد المعدل - 5 رسائل/دقيقة)
# ----------------------------------------------------------------------

# تخزين مؤقت لعدّ الطلبات لكل IP
# { 'ip_address': [timestamp1, timestamp2, ...] }
request_counts = {}
RATE_LIMIT_MESSAGES = 5
RATE_LIMIT_WINDOW_SECONDS = 60  # 1 minute

class OffensiveLanguageMiddleware:
    """
    3. Middleware لتحديد معدل الطلبات: 5 رسائل (POST) في الدقيقة لكل عنوان IP.
    (يُستخدم كبديل لتحديد اللغة المسيئة كما هو مقترح في المهمة).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # نركز فقط على طلبات POST (التي تُستخدم عادةً لإرسال رسالة دردشة)
        if request.method == 'POST':
            # الحصول على عنوان IP للعميل
            ip_address = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
            if not ip_address:
                # إذا لم نتمكن من الحصول على IP، يمكننا المتابعة أو الرفض
                ip_address = 'unknown' 

            current_timestamp = time.time()
            
            # تنظيف السجلات القديمة: إبقاء الطوابع الزمنية التي تقع ضمن النافذة الزمنية (60 ثانية)
            window_start = current_timestamp - RATE_LIMIT_WINDOW_SECONDS
            request_counts[ip_address] = [
                ts for ts in request_counts.get(ip_address, []) if ts > window_start
            ]

            # التحقق من عدد الطلبات المتبقية
            if len(request_counts[ip_address]) >= RATE_LIMIT_MESSAGES:
                # تجاوز الحد المسموح
                return HttpResponseForbidden("Rate limit exceeded: 5 messages per minute.")
            
            # تسجيل الطلب الجديد
            request_counts[ip_address].append(current_timestamp)
        
        response = self.get_response(request)
        return response

# ----------------------------------------------------------------------
# Task 4: فرض أذونات دور مستخدم الدردشة
# ----------------------------------------------------------------------

class RolePermissionMiddleware:
    """
    4. Middleware يتحقق من دور المستخدم (Admin/Moderator) قبل السماح بالوصول.
    يفترض وجود حقل 'role' في نموذج المستخدم (User Model) أو وجود طريقة للتحقق من الأدوار.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ALLOWED_ROLES = ['admin', 'moderator']
        # المسارات التي تتطلب صلاحيات خاصة (يمكن تحديدها بدقة أكبر في مشروع حقيقي)
        self.PROTECTED_PATHS = ['/admin/', '/chats/manage/', '/chats/delete/']

    def __call__(self, request):
        # التحقق من أن المستخدم مسجل الدخول
        if not request.user.is_authenticated:
            # إذا كان الطلب إلى مسار محمي ولم يكن المستخدم مسجلاً، ارفض
            if any(request.path.startswith(path) for path in self.PROTECTED_PATHS):
                 return HttpResponseForbidden("Access Denied: Login required for this action.")
            
        # التحقق من صلاحيات الدور للمسارات المحمية
        if any(request.path.startswith(path) for path in self.PROTECTED_PATHS):
            
            # افترض أن الدور موجود كخاصية 'role' في كائن المستخدم
            # في Django، يمكننا استخدام is_staff أو is_superuser أو المجموعات (Groups)
            
            # مثال باستخدام خصائص Django المدمجة (is_staff/is_superuser)
            if not (request.user.is_staff or request.user.is_superuser):
                # يمكنك تخصيص هذا التحقق بناءً على كيفية تعريف الأدوار 'admin' و 'moderator'
                return HttpResponseForbidden("Access Denied: Only Admin/Moderator users can access this resource.")

        response = self.get_response(request)
        return response