from django.contrib import admin
from .models import ChatRoom, RoomChatMessage


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'user1', 'user2']
    search_fields = ['id', 'user1__username', 'user2__username', 'user1__email', 'user2__email']
    readonly_fields = ['id',]


admin.site.register(ChatRoom, ChatRoomAdmin)


class RoomChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user', 'timestamp']


admin.site.register(RoomChatMessage, RoomChatMessageAdmin)
