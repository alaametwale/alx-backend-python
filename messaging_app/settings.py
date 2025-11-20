# messaging_app/settings.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'django_filters',
    'chats',  # تطبيق الرسائل
]

MIDDLEWARE = [
    # ...
]

ROOT_URLCONF = 'messaging_app.urls'

TEMPLATES = [
    # ...
]

WSGI_APPLICATION = 'messaging_app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DRF + django-filter settings
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # تعديل حسب متطلبات الأمان
    ),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'