from django.urls import path
from .views import MessageView, example, ChatUser

app_name = 'chat_messages'

urlpatterns = [
    path('api/messages/', example),
    path('api/messages/<int:message_id>', example),

    path('api/chat/', example),
    path('api/chat/<int:message_id>', example),
    path('api/chat/messages/<chat_id>/', MessageView.as_view()),
    path('api/chat/other-user/<int:chat_id>/', ChatUser.as_view()),

    path('api/users/', example),
    path('api/user/<int:chat_id>/', example),
]

# urlpatterns = [
#     # Messages API
#     path('api/messages/', example, name='message-list'),  # GET: список всех сообщений
#     path('api/messages/<int:message_id>/', example, name='message-detail'),
#     # GET: получить конкретное сообщение по его ID
#     # PUT: обновить конкретное сообщение
#     # PATCH: частично обновить конкретное сообщение
#     # DELETE: удалить конкретное сообщение
#
#     # Chat API
#     path('api/chat/', example, name='chat-list'),  # GET: список всех чатов
#     path('api/chat/<int:chat_id>/', example, name='chat-detail'),  # GET: получить конкретный чат по его ID
#     # PUT: обновить конкретный чат
#     # PATCH: частично обновить конкретный чат
#     # DELETE: удалить конкретный чат
#
#     path('api/chat/messages/<int:chat_id>/', MessageView.as_view(), name='chat-message-list'),
#     # GET: список всех сообщений в чате
#     # POST: создать новое сообщение в чате
#
#     path('api/chat/user/<int:user_id>/', example, name='chat-user-detail'),
#     # GET: получить информацию о конкретном пользователе в чате
#     # PUT: обновить информацию о конкретном пользователе в чате
#     # PATCH: частично обновить информацию о конкретном пользователе в чате
#     # DELETE: удалить конкретного пользователя из чата
#
#     # Users API
#     path('api/users/', example, name='user-list'),  # GET: список всех пользователей
#     path('api/user/<int:user_id>/', example, name='user-detail'),
#     # GET: получить информацию о конкретном пользователе по его ID
#     # PUT: обновить информацию о конкретном пользователе
#     # PATCH: частично обновить информацию о конкретном пользователе
#     # DELETE: удалить конкретного пользователя
# ]
