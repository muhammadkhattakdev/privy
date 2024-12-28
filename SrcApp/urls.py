from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='homepage'),
    path('create-room/', views.create_room, name='create-room'),
    path('messages/', views.chat_messages, name='messages'),
    path('room/<roomId>', views.chatRoom, name='chat_room'),
]



