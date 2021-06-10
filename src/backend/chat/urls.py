from django.urls import path

from .views import (
                    messenger,
                    room,
                    test
                    )

urlpatterns = [
    path('', messenger, name='messenger'),
    path('<str:room_name>/', room, name='room'),
]
