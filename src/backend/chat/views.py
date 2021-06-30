from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from itertools import chain

from .models import ChatRoom, RoomChatMessage
from .utils import calculate_date


@login_required(login_url='login')
def messenger(request):
    context = {}
    user = request.user

    rooms1 = ChatRoom.objects.filter(user1=user)
    rooms2 = ChatRoom.objects.filter(user2=user)

    rooms = list(chain(rooms1, rooms2))

    rooms_info = []
    for room in rooms:
        room_info = {}
        if room.user1 == user or room.user2 == user:
            room_info['room_id'] = room.id
            room_info['user'] = room.user2 if room.user1 == user else room.user1

            message = RoomChatMessage.objects.last_message_from_room(room)
            if message is not None:
                room_info['message'] = message.content
                room_info['message_time'] = calculate_date(message.timestamp)

            rooms_info.append(room_info)

    context['rooms_info'] = rooms_info

    return render(request, 'chat/messenger.html', context)
