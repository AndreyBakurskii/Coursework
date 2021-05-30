from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    context = dict()

    context['room_name'] = room_name
    return render(request, 'chat/room.html', context)


def test(request):
    return render(request, 'contact/chat.html')
