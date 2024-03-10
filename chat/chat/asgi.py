from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
import os
from django.core.asgi import get_asgi_application
from django.urls import path
from chat_messages.consumer import Consumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/', Consumer.as_asgi())
        ])
    )
})