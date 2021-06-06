import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Contact, ContactRequest
from account.models import Account


def my_contacts(request: HttpRequest):
    context = {}
    user = request.user

    context['friends'] = sorted(Contact.get_friends(user), key=lambda user: user.last_name)

    search_query = request.GET.get("q")
    # проверка на None
    if search_query:
        # проверка на непустой запрос
        search_query = search_query.strip()
        if len(search_query) > 0:
            context['friends'] = [user for user in context['friends']
                                  if f'{user.last_name} {user.first_name} {user.middle_name} {user.email}' \
                                     f' {user.username}'.find(search_query) != -1]

    context['senders_requests'] = ContactRequest.get_senders(user)

    return render(request, 'contact/contacts.html', context)


def define_relationship(request, from_func=False, *args, **kwargs):
    """
    Может быть 4 статуса отношений между двумя юзерами:
        - друзья (FRIENDS)
        - не друзья и нет запроса на дружбу (NO_RELATIONSHIP)
        - не друзья и должен принять запрос на дружбу (RECEIVER_REQUEST)
        - не друзья и отправил запрос на дружбу (SENDER_REQUEST)

    Возвращается отношение отностительно владельца аккаунта к запрашиваемому пользователю
    :param request:
    :param args:
    :param kwargs:
    :param from_func:
    :return:
    """
    # noinspection PyPep8Naming
    FRIENDS, NO_RELATIONSHIP, RECEIVER_REQUEST, SENDER_REQUEST = range(4)
    context = {}

    if request.POST or from_func:
        user1 = request.user

        user2_id = kwargs.get('user_id')
        user2 = None
        try:
            user2 = Account.objects.get(pk=user2_id)
        except Account.DoesNotExist:
            context['error'] = True
            return HttpResponse(json.dumps(context), content_type='application/json')

        context['relationship'] = None

        if Contact.get_contact(user1, user2):
            context['relationship'] = FRIENDS

        elif ContactRequest.get_request(user1, user2):
            context['relationship'] = SENDER_REQUEST

        elif ContactRequest.get_request(user2, user1):
            context['relationship'] = RECEIVER_REQUEST

        else:
            context['relationship'] = NO_RELATIONSHIP

        return HttpResponse(json.dumps(context), content_type='application/json')


def create_contact(request, *args, **kwargs):
    context = {}

    if request.POST:
        context['success'] = False
        user1 = request.user

        user2_id = kwargs.get('user_id')
        try:
            user2 = Account.objects.get(pk=user2_id)
        except Account.DoesNotExist:
            context['error'] = True
            return HttpResponse(json.dumps(context), content_type='application/json')

        if ContactRequest.create_request(user1, user2):
            context['success'] = True
            return HttpResponse(json.dumps(context), content_type='application/json')

        return HttpResponse(json.dumps(context), content_type='application/json')


def check_is_friend(request, *args, **kwargs):
    context = {}

    if request.POST:
        user_id = kwargs.get('user_id')
        context['is_friend'] = False

        try:
            user = Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return HttpResponse(json.dumps(context), content_type='application/json')

        if Contact.get_contact(request.user, user):
            context['is_friend'] = True

        return HttpResponse(json.dumps(context), content_type='application/json')


def delete_contact(request, *args, **kwargs):
    context = {}

    if request.POST:
        context['success'] = False
        user1 = request.user

        user2_id = kwargs.get('user_id')
        try:
            user2 = Account.objects.get(pk=user2_id)
        except Account.DoesNotExist:
            return HttpResponse(json.dumps(context), content_type='application/json')

        Contact.delete_contact(user1, user2)

        context['success'] = True

        return HttpResponse(json.dumps(context), content_type='application/json')


def accept_request(request, *args, **kwargs):
    context = {}

    if request.POST:
        context['success'] = False

        sender_id = kwargs.get('user_id')
        try:
            sender = Account.objects.get(pk=sender_id)
        except Account.DoesNotExist:
            return HttpResponse(json.dumps(context), content_type='application/json')

        receiver = request.user

        contact_request = ContactRequest.get_request(sender, receiver)
        if contact_request:
            contact_request.accept()
            context['success'] = True

        return HttpResponse(json.dumps(context), content_type='application/json')


def decline_request(request, *args, **kwargs):
    context = {}

    if request.POST:
        context['success'] = False

        sender_id = kwargs.get('user_id')
        try:
            sender = Account.objects.get(pk=sender_id)
        except Account.DoesNotExist:
            return HttpResponse(json.dumps(context), content_type='application/json')

        receiver = request.user

        contact_request = ContactRequest.get_request(sender, receiver)
        if contact_request:
            contact_request.decline()
            context['success'] = True

        return HttpResponse(json.dumps(context), content_type='application/json')


def cancel_request(request, *args, **kwargs):
    context = {}

    if request.POST:
        context['success'] = False

        user1 = request.user

        user2_id = kwargs.get('user_id')
        try:
            user2 = Account.objects.get(pk=user2_id)
        except Account.DoesNotExist:
            return HttpResponse(json.dumps(context), content_type='application/json')

        contact_request = ContactRequest.get_request(user1, user2)
        if contact_request:
            contact_request.decline()
            context['success'] = True

        return HttpResponse(json.dumps(context), content_type='application/json')
