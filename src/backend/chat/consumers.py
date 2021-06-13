import json
from channels.generic.websocket import AsyncWebsocketConsumer

from time import sleep


class ChatConsumer(AsyncWebsocketConsumer):

    """
        Команды от клиента:
            подключение -                   "join";
            отключение -                    "leave";
            отправка сообщения -            "send";
            получение старых сообщений -    "get_old_messages";
    """

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # sleep(2)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # Receive message from WebSocket
    async def receive(self, text_data):
        content = json.loads(text_data)
        command = content.get("command", None)

        print(command)
        # обработка ошибок

        if command == "send":
            message = content["message"]

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        data = json.dumps({
            'message': message
        })

        # Send message to WebSocket
        await self.send(data)
