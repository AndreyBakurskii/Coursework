from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    # users in room
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_user2')

    # online_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='online_users')

    # def connect_user(self, user):
    #     is_online = False
    #     if user not in self.online_users.all():
    #         self.online_users.add(user)
    #         is_online = True
    #
    #     return is_online
    #
    # def disconnect_user(self, user):
    #     is_offline = False
    #     if user in self.online_users.all():
    #         self.online_users.remove(user)
    #         is_offline = True
    #
    #     return is_offline

    @property
    def group_name(self):
        return f'ChatRoom-{self.id}'


class RoomChatMessageManager(models.Manager):
    def from_room(self, room, from_message_id=None):
        query_set = RoomChatMessage.objects.filter(room=room).order_by("-timestamp")

        if from_message_id is not None:
            query_set = query_set.filter(id__lt=from_message_id)
        return query_set

    def last_message_from_room(self, room):
        try:
            last_message = RoomChatMessage.objects.from_room(room).latest('id')
        except RoomChatMessage.DoesNotExist:
            return None

        return last_message


class RoomChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    objects = RoomChatMessageManager()

    def __str__(self):
        return self.content
