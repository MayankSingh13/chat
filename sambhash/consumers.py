import json
import datetime
from channels.generic.websocket import AsyncWebsocketConsumer

online_users = []

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.path = self.scope['path']
        self.room_group_name = self.path[10:-1]
        print(self.room_group_name)
        online_users.append(self.user.first_name)
        print(online_users)
        #print(self.user.first_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Send message to room group on getting connected.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join_message',
                'message': 'New user entered.',
                'on_user': online_users,
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        online_users.remove(self.user.first_name)
        print(online_users)

        # Send message to room group on leaving.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'leave_message',
                'message': 'New user entered.',
                'on_user': online_users,
            }
        )
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']
        user = text_data_json['user']
        #print(message)
        #print(user)
        #online_users = []
        now = datetime.datetime.now().strftime('%H:%M:%S')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'time': now
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        time = event['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'time': time
        }))


    # Receive message from room group on getting connected
    async def join_message(self, event):
        message = event['message']
        on_user = event['on_user']

        await self.send(text_data=json.dumps({
            'message': message,
            'on_user': on_user
        }))

    async def leave_message(self, event):
        message = event['message']
        on_user = event['on_user']

        await self.send(text_data=json.dumps({
            'message': message,
            'on_user': on_user
        }))
