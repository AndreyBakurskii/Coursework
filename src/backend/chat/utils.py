from django.core.serializers.python import Serializer
from django.contrib.humanize.templatetags.humanize import naturalday
from datetime import datetime

class LazyRoomChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'sender_id': str(obj.user.id)})
        dump_object.update({'message_id': str(obj.id)})
        dump_object.update({'message': str(obj.content)})
        return dump_object


def calculate_date(timestamp):
    date = ""

    if naturalday(timestamp) == 'today':
        date = f"{datetime.strftime(timestamp, '%H:%M')}"
    elif naturalday(timestamp) == 'yesterday':
        date = f"Вчера"
    else:
        date = f"{datetime.strftime(timestamp, '%d.%m')}"

    print(date)
    return date
