from django.db import models
from django.contrib.auth import get_user_model


class Chat(models.Model):
    user1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='chats_as_user1')
    user2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='chats_as_user2')

    def __str__(self):
        return f'{self.user1} and {self.user2}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} write: {self.content}'
