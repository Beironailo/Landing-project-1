import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime


class ChatConsumer(AsyncWebsocketConsumer):

    rooms = dict()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        user = str(self.user)
        if user == 'AnonymousUser':
            user = 'Guest'
        if self.room_name not in self.rooms:
            self.rooms[self.room_name] = {'log': []}
        self.rooms[self.room_name]['log'].append((user, now, message))
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'message': message,
                    'time': now,
                    'user': user
                },
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']['message']
        now = event['message']['time']
        user = event['message']['user']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': {
                    'message': message,
                    'time': now,
                    'user': user
                },
        }))


class AdminChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_group_name = 'admin_room'
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room = text_data_json['room']
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        user = str(self.user)
        if user == 'AnonymousUser':
            user = 'Guest'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_catcher',
                'message': {
                    'message': message,
                    'time': now,
                    'user': user,
                    'room': room
                },
            }
        )

    async def room_catcher(self, event):
        message = event['message']['message']
        now = event['message']['time']
        user = event['message']['user']
        room = event['message']['room']
        await self.send(text_data=json.dumps({
            'message': {
                    'message': message,
                    'time': now,
                    'user': user,
                    'room': room
                },
        }))