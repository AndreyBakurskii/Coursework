from django.core.serializers.python import Serializer
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils.timezone import pytz
from backend.settings import TIME_ZONE


class LazyRoomChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'sender_id': str(obj.user.id)})
        dump_object.update({'message_id': str(obj.id)})
        dump_object.update({'message': str(obj.content)})
        return dump_object


def calculate_date(timestamp):
    date = ""

    timestamp = timestamp.astimezone(pytz.timezone(TIME_ZONE))

    if naturalday(timestamp) == 'today':
        date = f"{timestamp.hour}:{timestamp.minute}"
    elif naturalday(timestamp) == 'yesterday':
        date = f"Вчера"
    else:
        date = f"{timestamp.day}.{timestamp.month}"

    return date
