
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls', namespace='dashboard')),
    path('', include('customuser.urls', namespace='customuser')),
    path('', include('chat_messages.urls', namespace='chat_messages')),
    path('', include('API_chat.urls', namespace='API_chat')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
