<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
=======
# chats/urls.py
from django.urls import path

# لا يوجد مسارات API حتى الآن، لكن هذا الملف ضروري لتجنب خطأ الاستيراد.
urlpatterns = [
    # path('messages/', views.MessageListCreate.as_view(), name='message-list'),
]
>>>>>>> 3a649449a61a17ea5d3214c20863e67fb301673f
