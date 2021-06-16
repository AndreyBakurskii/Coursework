from django.core.serializers.python import Serializer


class LazyRoomChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'sender_id': str(obj.user.id)})
        dump_object.update({'message_id': str(obj.id)})
        dump_object.update({'message': str(obj.content)})
        return dump_object
