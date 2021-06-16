import json
from time import sleep

from django.core.paginator import Paginator

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from account.models import Account
from .models import ChatRoom, RoomChatMessage
from .constants import *
from .utils import LazyRoomChatMessageEncoder


class ChatConsumer(AsyncWebsocketConsumer):

    """
        Команды от клиента:
            подключение -                   "join";
            отключение -                    "leave";
            отправка сообщения -            "send";
            получение старых сообщений -    "get_old_messages";
    """

    async def connect(self):
        self.room_id = None

        await self.accept()

    # Receive message from WebSocket
    async def receive(self, text_data):
        content = json.loads(text_data)
        command = content.get("command", None)

        print(command)
        # обработка ошибок
        if command == "join":
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            self.user = Account.objects.get(email=str(self.scope['user']))
            self.room_id = self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            room = await get_room_or_error(self.room_id, self.user)

            # отправляем сообщение на клиент, об успешном соединении
            data = json.dumps({
                'join': str(room.id)
            })

            await self.send(data)

        elif command == "send":
            message = content["message"]

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )

        elif command == "get_old_messages":
            room = await get_room_or_error(self.room_id, self.user)

            from_message_id = content.get('from_massage_id', None)

            payload = await get_old_messages(room, from_message_id=from_message_id)
            if payload is not None:
                payload = json.loads(payload)

                await self.send_old_messages(payload['messages'])

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
            'message': message,
            'sender_id': self.user.id,
        })
        room = await get_room_or_error(self.room_id, self.user)

        await create_room_chat_message(room, self.user, message)

        # Send message to WebSocket
        await self.send(data)

    async def send_old_messages(self, messages):

        data = json.dumps({
            'get_old_messages': 'get_old_messages',
            'messages': messages,
            'sender_id': self.user.id,
        })

        await self.send(data)


@database_sync_to_async
def create_room_chat_message(room, user, message):
    return RoomChatMessage.objects.create(user=user, room=room, content=message)


@database_sync_to_async
def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    try:
        room = ChatRoom.objects.get(pk=room_id)

    except ChatRoom.DoesNotExist:
        raise Exception("Room invalid")

    if room.user1 != user and room.user2 != user:
        raise Exception("room access denied")
    return room


@database_sync_to_async
def get_old_messages(room, from_message_id=None):
    try:
        qs = RoomChatMessage.objects.from_room(room, from_message_id=from_message_id)
        payload = {}
        if qs:
            p = Paginator(qs, DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE)

            s = LazyRoomChatMessageEncoder()
            payload['messages'] = s.serialize(p.page(1).object_list)
        else:
            payload['messages'] = "None"
        return json.dumps(payload)

    except Exception as e:
        print("EXCEPTION: " + str(e))
    return None
