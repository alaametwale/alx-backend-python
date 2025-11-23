# chats/middleware.py
from datetime import datetime
import os

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # تحديد مسار ملف اللوج
        self.log_file = os.path.join(os.path.dirname(__file__), 'requests.log')

    def __call__(self, request):
        # تحديد المستخدم
        user = request.user if request.user.is_authenticated else 'Anonymous'
        # تكوين رسالة اللوج
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        # تسجيل الرسالة في الملف
        with open(self.log_file, 'a') as f:
            f.write(log_message)
        # متابعة الطلب
        response = self.get_response(request)
        return response
