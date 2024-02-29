import json

from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async


class YourConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data):
        await self.send({
            "type": "websocket.send",
            "text": "Hello from Django socket"
        })

    async def websocket_disconnect(self, event):
        pass


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Принимаем WebSocket-соединение
        await self.accept()

        # Получаем ID чата из URL (ваша логика может отличаться)
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        # Создаем имя группы для данного чата
        self.chat_group_name = f'chat_{self.chat_id}'
        print(self.chat_id,self.chat_group_name)

        # Присоединяем клиента к группе чата
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Отключаем клиента от группы чата
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Получаем текст сообщения от клиента
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']

        chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)
        sender = await sync_to_async(get_user_model().objects.get)(id=user_id)
        new_message = await sync_to_async(Message.objects.create)(content=message, chat=chat, sender=sender)
        await sync_to_async(new_message.save)()
        # Отправляем сообщение в группу чата
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'content': new_message.content,
                    'id': new_message.id,
                    'timestamp': new_message.timestamp.isoformat(),
                    'sender': {
                        'id': sender.id,
                        'nickname': sender.nickname
                    }

                }
            }
        )

    async def chat_message(self, event):
        # Отправляем сообщение обратно клиенту
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
