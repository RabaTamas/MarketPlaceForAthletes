from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("", views.chat, name="room"),
    path("get_conversation/", views.getConversation, name="get_conversation"),
    path('<int:pk>/', views.chat, name='room'),
    path("get_chats/", views.getChats, name="get_chats")
]
