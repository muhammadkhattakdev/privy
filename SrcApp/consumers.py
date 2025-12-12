# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import redis
import uuid
from cryptography.fernet import Fernet

class ChatConsumer(AsyncWebsocketConsumer):

    def encrypt_message(self, key, message):
        fernet = Fernet(key)
        return fernet.encrypt(message.encode()).decode()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'{self.room_name}'
        print(self.room_name)
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

        self.redis.incr(f"{self.room_group_name}_connections")

        key = self.redis.get(f"{self.room_group_name}_key")

        if not key:
            key = Fernet.generate_key()
            self.redis.set(f"{self.room_group_name}_key", key)

        print('key is',key)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):

        remaining_connections = self.redis.decr(f"{self.room_group_name}_connections")
        print(remaining_connections)
        if remaining_connections <= 0:
            self.redis.delete(self.room_group_name)
            self.redis.delete(f"{self.room_group_name}_connections")
            print('deleted')
        print(f"Disconnected from room: {self.room_group_name}, with close code: {close_code}")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
    
        message = text_data_json['message']
        time = text_data_json['time']
        key = self.redis.get(f"{self.room_group_name}_key")
        if not key:
            print("Error: Encryption key not found for room.")
            return

        encrypted_message = self.encrypt_message(key, message)

        r = redis.Redis(host='localhost', port=6379, db=0)
        message_data = {'message': encrypted_message, 'time': time}

        print(self.room_group_name)
        r.lpush(self.room_group_name, json.dumps(message_data))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'time': time,
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        time = event['time']

        await self.send(text_data=json.dumps({
            'message': message,
            'time': time
        }))

    