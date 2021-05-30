from django.db import models
from django.conf import settings


class Contact(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user2')

    @staticmethod
    def get_friends(user: settings.AUTH_USER_MODEL):
        friend = []
        for contact in Contact.objects.all():
            if contact.user1 == user:
                friend.append(contact.user2)
            elif contact.user2 == user:
                friend.append(contact.user1)

        return friend

    @staticmethod
    def create_contact(user1, user2):
        contact1 = Contact(user1=user1, user2=user2)
        contact1.save()

    @staticmethod
    def delete_contact(owner, del_friend):
        Contact.objects.filter(user1=owner, user2=del_friend).delete()
        Contact.objects.filter(user1=del_friend, user2=owner).delete()


class ContactRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')

    is_active = models.BooleanField(blank=True, null=False, default=True)

    def accept(self):
        Contact.create_contact(self.sender, self.receiver)

        self.is_active = False

    def decline(self):
        self.is_active = False

    @staticmethod
    def create_request(sender, receiver):
        contact_request = ContactRequest(sender=sender, receiver=receiver)
        contact_request.save()

    @staticmethod
    def get_senders(user):
        """
        Возвращает список поль-лей которые отправили запрос для user
        :param user:
        :return:
        """

        return [request.sender for request in ContactRequest.objects.filter(receiver=user)]

    @staticmethod
    def get_request(sender, receiver):
        return ContactRequest.objects.get(sender=sender, receiver=receiver)