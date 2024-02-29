from django.shortcuts import render
from django.db.models import Q
from chat_messages.models import Chat


def dashboard(request):
    user_chats = Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user))

    chats_with_messages = []
    if user_chats:
        for chat in user_chats:
            last_message = chat.messages.order_by('-timestamp').first()
            other_user = chat.user1 if chat.user2 == request.user else chat.user2
            chat_info = {
                'chat': chat,
                'last_message': last_message,
                'other_user_username': other_user.nickname,
                # 'other_user_avatar': other_user.avatar.url if other_user.avatar else '/path/to/default/avatar.jpg',
            }
            chats_with_messages.append(chat_info)
    return render(request, 'dashboard/dashboard.html', {'chats_with_messages': chats_with_messages})
