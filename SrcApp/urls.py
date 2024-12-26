from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('messages/', views.chat_messages, name='messages'),
    path('room/<roomId>', views.chatRoom, name='chat_room'),
]

