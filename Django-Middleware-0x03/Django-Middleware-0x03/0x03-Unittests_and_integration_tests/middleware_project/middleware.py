import logging
from datetime import datetime

INSTALLED_APPS = [
    ...
    'chats',
]

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s"
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)
'chats.middleware.RequestLoggingMiddleware',
