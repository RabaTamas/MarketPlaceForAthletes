from members.models import Profile
from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.core.exceptions import ObjectDoesNotExist
from items.models import Item
# Create your models here.

class Chat(models.Model):
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participant1")
    item = models.ForeignKey(Item,on_delete=models.CASCADE, related_name="item" )
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participant2")
    lastupdated = models.DateTimeField(auto_now = True)
    
    class Meta:
        UniqueConstraint(fields=["participant1", "participant2", "item"], name="participants_item_unique_together")

        ordering = ['-lastupdated']

    @staticmethod
    def GetChatByParticipants(participant1, participant2, item, saveifnotexists = True):
        if participant1.pk < participant2.pk:
            participant2, participant1 = participant1, participant2
        try:
            return Chat.objects.get(participant1 = participant1, participant2 = participant2, item = item)
        except ObjectDoesNotExist:
            if saveifnotexists:
                return Chat.objects.create(participant1 = participant1, participant2 = participant2, item = item)
            return Chat(participant1 = participant1, participant2 = participant2, item = item)
    
    @staticmethod
    def GetChatByParticipant(participant):
        return Chat.objects.filter(participant1 = participant) | Chat.objects.filter(participant2 = participant)
    
    @staticmethod
    def GetChatByItemAndParticipant(item, participant):
        return Chat.objects.filter(participant1 = participant, item = item) | Chat.objects.filter(participant2 = participant, item = item)
        #return Chat.objects.filter(item = item)

    @staticmethod
    def GetChatById(id):
        try:
            return Chat.objects.get(pk = id)
        except:
            raise ObjectDoesNotExist()
    
    def GetMessages(self):
        return self.msgs.all().order_by("timestamp")
        

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="msgs")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_msgs")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_msgs")
    content = models.TextField()
    timestamp = models.DateTimeField()
    isread = models.BooleanField(default=False)