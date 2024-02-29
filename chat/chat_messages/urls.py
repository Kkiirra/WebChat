from django.urls import path
from .views import get_users_messages, get_current_user, get_current_chat_user

app_name = 'chat_messages'

urlpatterns = [
    path('api/chat-messages/<int:chat_id>/current-user/', get_users_messages),
    path('api/current-user/', get_current_user),
    path('api/get_current_chat_user/<int:chat_id>/', get_current_chat_user),

]
