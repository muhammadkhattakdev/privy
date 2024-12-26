# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import redis

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Get the room name from the URL route
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print('this id is', self.room_name)
        # Accept the WebSocket connection
        print(f"Connecting to room: {self.room_group_name}")
        await self.accept()

    async def disconnect(self, close_code):
        # Handle the disconnection from WebSocket
        print(f"Disconnected from room: {self.room_group_name}, with close code: {close_code}")
        await self.close()
    async def receive(self, text_data):
        # Handle the incoming message from the WebSocket
        text_data_json = json.loads(text_data)
    
    # Extract the message and time from the incoming data
        message = text_data_json['message']
        time = text_data_json['time']

        # Store the message in Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        message_data = {'message': message, 'time': time}
        r.lpush(self.room_group_name, json.dumps(message_data))  # Store message in Redis list

        # Send a message back to the WebSocket (optional for feedback)
        await self.send(text_data=json.dumps({
            'message': message,
            'time': time
        }))

    