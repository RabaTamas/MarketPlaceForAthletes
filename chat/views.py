from django.shortcuts import render
from .models import Chat
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.contrib.auth.models import User
from items.models import Item
# Create your views here.

@login_required
def chat(request, pk = None):
    return render(request, "room.html", {"sender": request.user.pk})

@login_required
def getChats(request):
    chats = Chat.GetChatByParticipant(request.user)
    output = []
    try:
        item = Item.objects.filter(pk = request.GET["itempk"]).first()
        if not Chat.GetChatByItem(item):
            empty_chat = Chat.GetChatByParticipants(request.user, item.advertiser.user, item, False)
            output.append({
                "pk": empty_chat.pk,
                "item": {"pk": empty_chat.item.pk, "name": f"{empty_chat.item.name}", "imagepath": f"{empty_chat.item.image.url}"},
                "participant1": {"pk": empty_chat.participant1.pk, "name": f"{empty_chat.participant1.first_name} {empty_chat.participant1.last_name}"},
                "participant2": {"pk": empty_chat.participant2.pk, "name": f"{empty_chat.participant2.first_name} {empty_chat.participant2.last_name}"},
                "last_message": ""
            })
    except:
        pass
    for chat in chats:
        message = chat.GetMessages().last()
        last_message = {
            "message": message.content,
            "receiver": {"pk": message.receiver.pk, "name": f"{message.receiver.first_name} {message.receiver.last_name}"},
            "sender": {"pk": message.sender.pk, "name": f"{message.sender.first_name} {message.sender.last_name}"},
            "timestamp": str(message.timestamp)
        }
        output.append({
            "pk": chat.pk,
            "item": {"pk": chat.item.pk, "name": f"{chat.item.name}", "imagepath": f"{chat.item.image.url}"},
            "participant1": {"pk": chat.participant1.pk, "name": f"{chat.participant1.first_name} {chat.participant1.last_name}"},
            "participant2": {"pk": chat.participant2.pk, "name": f"{chat.participant2.first_name} {chat.participant2.last_name}"},
            "last_message": last_message
        })
    
    return JsonResponse({"chats": json.dumps(output)})
    
@login_required
def getConversation(request):
    chat_id = request.GET.get('chat_id')
    print("chat_id is ", chat_id)
    output = []
    try:
        chat = Chat.GetChatById(int(chat_id))
        messages = chat.GetMessages()
        for message in messages:
            if message.receiver == request.user and message.isread == False:
                message.isread = True
                message.save()
        messages = chat.GetMessages()
        for message in messages:
            output.append({
                "message": message.content,
                "receiver": {"pk": message.receiver.pk, "name": f"{message.receiver.first_name} {message.receiver.last_name}"},
                "sender": {"pk": message.sender.pk, "name": f"{message.sender.first_name} {message.sender.last_name}"},
                "timestamp": str(message.timestamp),
                "isread": message.isread
            })
    except:
        pass
    return JsonResponse({"messages": json.dumps(output)})