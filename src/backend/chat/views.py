from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def messenger(request):
    return render(request, 'chat/messenger.html')


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    context = dict()

    context['room_name'] = room_name
    return render(request, 'chat/room.html', context)


def test(request):
    return render(request, 'contact/chat.html')
