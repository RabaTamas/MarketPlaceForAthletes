import json
from django.test import TestCase
from django.contrib.auth.models import User
from items.models import Item, Sport, ItemCondition
from chat.models import Chat, ChatMessage
from members.models import Profile

class ChatModelTests(TestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="testpassword")
        self.user2 = User.objects.create_user(username="user2", password="testpassword")
        # Create profiles
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)
        # Create sport and condition
        self.sport = Sport.objects.create(name="Football")
        self.condition = ItemCondition.objects.create(name="New")
        # Create an item
        self.item = Item.objects.create(
            name="Football Ball",
            sport=self.sport,
            advertiser=self.profile1,
            description="A brand new football",
            price=20.0,
            condition=self.condition,
        )

    def test_chat_creation(self):
        # Test chat creation via static method
        chat = Chat.GetChatByParticipants(self.user1, self.user2, self.item)
        self.assertIsNotNone(chat)
        self.assertEqual(chat.participant1, self.user2)
        self.assertEqual(chat.participant2, self.user1)
        self.assertEqual(chat.item, self.item)
        self.assertTrue(Chat.objects.filter(pk=chat.pk).exists())

    def test_get_chat_by_participant(self):
        # Create a chat
        Chat.GetChatByParticipants(self.user1, self.user2, self.item)
        chats = Chat.GetChatByParticipant(self.user1)
        self.assertEqual(len(chats), 1)

    def test_get_chat_messages(self):
        # Create a chat and add messages
        chat = Chat.GetChatByParticipants(self.user1, self.user2, self.item)
        message1 = ChatMessage.objects.create(
            chat=chat,
            sender=self.user1,
            receiver=self.user2,
            content="Hello!",
            timestamp="2024-10-08T10:00:00Z",
        )
        message2 = ChatMessage.objects.create(
            chat=chat,
            sender=self.user2,
            receiver=self.user1,
            content="Hi there!",
            timestamp="2024-10-08T10:05:00Z",
        )
        messages = chat.GetMessages()
        self.assertEqual(messages.count(), 2)
        self.assertEqual(messages[0], message1)

class ChatViewTests(TestCase):

    def setUp(self):
        # Reuse the setup from ChatModelTests
        self.user1 = User.objects.create_user(username="user1", password="testpassword")
        self.user2 = User.objects.create_user(username="user2", password="testpassword")
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)
        self.sport = Sport.objects.create(name="Football")
        self.condition = ItemCondition.objects.create(name="New")
        self.item = Item.objects.create(
            name="Football Ball",
            sport=self.sport,
            advertiser=self.profile1,
            description="A brand new football",
            price=20.0,
            condition=self.condition,
        )
        self.client.login(username="user1", password="testpassword")

    def test_get_chats(self):
        # Test getChats view
        Chat.GetChatByParticipants(self.user1, self.user2, self.item)
        response = self.client.get("/chat/get_chats/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("chats", data)

    def test_get_conversation(self):
        # Test getConversation view
        chat = Chat.GetChatByParticipants(self.user1, self.user2, self.item)
        response = self.client.get(f"/chat/get_conversation/?chat_id={chat.id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("messages", data)

    def test_chat_view(self):
        response = self.client.get("/chat/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "room.html")
        self.assertEqual(response.context["sender"], self.user1.pk)

    