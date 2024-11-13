import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.auth import get_user
from channels.exceptions import StopConsumer
from items.models import Item
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

from .models import Chat, ChatMessage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.user.pk
        self.room_group_name = "chat_%s" % self.room_name
        print(self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        self.close()
        

    def receive(self, text_data):
        self.user = self.scope['user']        
        text_data_json = json.loads(text_data)
        
        sender = User.objects.filter(pk = int(text_data_json['sender'])).first()
        item = Item.objects.filter(pk = int(text_data_json['item'])).first()
        receiver = None
        try:
            receiver = User.objects.filter(pk = int(text_data_json['receiver'])).first()
        except:
            receiver = item.advertiser.user
        participant1 = sender
        participant2 = receiver
        print(text_data_json['item'])
        chat = Chat.GetChatByParticipants(participant1, participant2, item, True) #None
        
        message_string = text_data_json["message"]
        
        ChatMessage.objects.create(
            chat = chat,
            sender = sender,
            receiver = receiver,
            content = message_string,
            timestamp = datetime.now()
        )

            
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

@receiver(post_save, sender=ChatMessage)
def tmp(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_names = ["chat_%s" % instance.sender_id, "chat_%s" % instance.receiver_id]
        message_chat = instance.chat.pk
        message_string = instance.content
        message_sender = {"pk": instance.sender.pk, "name": f"{instance.sender.first_name} {instance.sender.last_name}"}
        message_receiver = {"pk": instance.receiver.pk, "name": f"{instance.receiver.first_name} {instance.receiver.last_name}"}
        message_timestamp = str(instance.timestamp)
        for group_name in group_names:
            async_to_sync(channel_layer.group_send)(group_name, {"type": "chat_message", "chat": message_chat, "message": message_string, "receiver": message_receiver, "sender": message_sender, "timestamp": message_timestamp})
