import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    """Подключение пока по комнатам, надо сделать, чтобы как-то автоматом подключалось для каждого пользователя"""

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
        if user is 'AnonymousUser':
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
                    'user': user,
                    'channel_name': self.channel_name
                },
        }))
