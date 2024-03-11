from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer


class CustomAuthToken(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        nickname = request.data.get('nickname')
        password = request.data.get('password')

        user = authenticate(nickname=nickname, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
