from rest_framework import serializers
from .models import Message
from django.contrib.auth import get_user_model
from customuser.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'nickname', 'last_login', 'is_online']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'timestamp']


