from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message, Chat
from .serializer import MessageSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from customuser.models import CustomUser


@api_view(['GET'])
def get_current_user_messages(request, chat_id):
    messages = Message.objects.filter(chat_id=chat_id, sender=request.user).order_by(F('timestamp').asc())
    serializer = MessageSerializer(messages, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_users_messages(request, chat_id):
    messages = Message.objects.filter(chat_id=chat_id)
    serializer = MessageSerializer(messages, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    serialized_user = UserSerializer(user)
    return Response(serialized_user.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_chat_user(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    if chat.user1 == request.user:
        other_user = chat.user2
    else:
        other_user = chat.user1
    user = other_user
    serialized_user = UserSerializer(user)
    return Response(serialized_user.data, status=status.HTTP_200_OK)
