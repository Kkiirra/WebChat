
import json
from django.utils import timezone
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from chat_messages.models import Message, Chat
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async, async_to_sync
from .redis_operations import get_channel_name, save_channel_name, get_all_channel_names


class Consumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.users_list = None

        user_id = self.user.id
        channel_name = self.channel_name
        save_channel_name(user_id, channel_name)

        await self.accept()

    async def disconnect(self, code):
        self.user.is_online = False
        self.user.last_login = timezone.now()
        await sync_to_async(self.user.save)()

        for user_id in self.users_list:
            channel_name = get_channel_name(user_id)

            if channel_name:
                await self.channel_layer.send(
                    channel_name,
                    {
                        'type': 'user.isonline',
                        'user_id': self.user.id,
                        'user_id_new': self.user.nickname,
                        'is_online': False,
                    }
                )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'user_status':
            chat_user_map = text_data_json.get('chat_user_map', None)

            self.users_list = chat_user_map.keys()

            for user_id in self.users_list:

                channel_name = get_channel_name(user_id)

                self.user.is_online = True
                await sync_to_async(self.user.save)()

                if channel_name:
                    await self.channel_layer.send(
                        channel_name,
                        {
                            'type': 'user.isonline',
                            'user_id': self.user.id,
                            'user_id_new': self.user.nickname,
                            'is_online': True,
                        }
                    )
        elif message_type == 'new_message':
            pass
        else:
            pass

    async def user_isonline(self, event):
        def_type = event['type']
        user_id = event['user_id']
        is_online = event['is_online']
        user_id_new = event['user_id_new']

        await self.send(text_data=json.dumps({
            'type': def_type,
            'user_id': user_id,
            'is_online': is_online,
            'user_id_new': user_id_new,

        }))

    # async def connect(self):
    #     # Принимаем WebSocket-соединение
    #     await self.accept()
    #
    #     self.user = self.scope['user']
    #     self.chat_group_name = '4'
    #     # await self.channel_layer.group_add(
    #     #     self.chat_group_name,
    #     #     self.channel_name
    #     # )
    #
    #     if self.user.is_authenticated:
    #         await self.update_user_status(True)
    #
    # async def disconnect(self, close_code):
    #     # Отключаем клиента от группы чата
    #     await self.update_user_status(False)
    #
    #     await self.channel_layer.group_discard(
    #         self.chat_group_name,
    #         self.channel_name
    #     )
    #
    # async def receive(self, text_data):
    #     # Получаем текст сообщения от клиента
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json.get('message', 0)
    #     user_id = text_data_json['user_id']
    #
    #     chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)
    #     sender = await sync_to_async(get_user_model().objects.get)(id=user_id)
    #     new_message = await sync_to_async(Message.objects.create)(content=message, chat=chat, sender=sender)
    #     await sync_to_async(new_message.save)()
    #     # Отправляем сообщение в группу чата
    #     await self.channel_layer.group_send(
    #         self.chat_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': {
    #                 'content': new_message.content,
    #                 'id': new_message.id,
    #                 'timestamp': new_message.timestamp.isoformat(),
    #                 'sender': {
    #                     'id': sender.id,
    #                     'nickname': sender.nickname
    #                 }
    #
    #             }
    #         }
    #     )
    #
    # async def chat_message(self, event):
    #     # Отправляем сообщение обратно клиенту
    #     message = event['message']
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
    #
    # async def user_status(self, event):
    #     message = event['user_id']
    #     is_online = event['is_online']
    #     nickname = event['nickname']
    #
    #     await self.send(text_data=json.dumps({
    #         'message': message,
    #         'is_online': is_online,
    #         'nickname': nickname,
    #     }))
    #
    # @sync_to_async
    # def update_user_status(self, is_online):
    #     # Обновление статуса пользователя в базе данных
    #     user, created = get_user_model().objects.get_or_create(id=self.user.id)
    #     user.is_online = is_online
    #     user.save()
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.chat_group_name,
    #         {
    #             'type': 'user_status',
    #             'user_id': user.id,
    #             'is_online': is_online,
    #             'nickname': user.nickname,
    #         }
    #     )
