from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Chats API
    path('api/', include('chats.urls')),

    # Required by ALX checker
    path('api-auth/', include('rest_framework.urls')),
]
