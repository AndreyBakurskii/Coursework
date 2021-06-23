from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from itertools import chain

from .models import ChatRoom, RoomChatMessage


@login_required(login_url='login')
def messenger(request):
    context = {}
    user = request.user

    rooms1 = ChatRoom.objects.filter(user1=user)
    rooms2 = ChatRoom.objects.filter(user2=user)

    rooms = list(chain(rooms1, rooms2))

    room_id_and_user = []
    for room in rooms:
        if room.user1 == user:
            room_id_and_user.append({'room_id': room.id, 'user': room.user2})
        else:
            room_id_and_user.append({'room_id': room.id, 'user': room.user1})

    context['room_id_and_user'] = room_id_and_user

    return render(request, 'chat/messenger.html', context)
