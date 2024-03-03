from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from asgiref.sync import sync_to_async
from .models import Message, Chat
from .serializer import MessageSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


class MessageView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        messages = Message.objects.filter(chat_id=chat_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        messages = Message.objects.filter(chat_id=chat_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatUser(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_id = kwargs.get('chat_id')
        chat = Chat.objects.get(id=chat_id)

        if request.user == chat.user1:
            other_user = chat.user2
        else:
            other_user = chat.user1

        serializer = UserSerializer(other_user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


def example(request):
    data = []
    return Response(data, status=status.HTTP_200_OK)