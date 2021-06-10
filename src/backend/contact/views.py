import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Contact, ContactRequest
from account.models import Account


@login_required(login_url='login')
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


@login_required(login_url='login')
def define_relationship(request: HttpRequest, from_func=False, *args, **kwargs):
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
            return HttpResponse(status=404)

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


@login_required(login_url='login')
def create_contact(request: HttpRequest, *args, **kwargs):
    context = {}

    if request.POST:
        user1 = request.user

        user2_id = kwargs.get('user_id')
        try:
            user2 = Account.objects.get(pk=user2_id)
        except Account.DoesNotExist:
            return HttpResponse(status=404)

        if ContactRequest.create_request(user1, user2) is None:
            return HttpResponse(status=404)

        return HttpResponse(json.dumps(context), content_type='application/json')


@login_required(login_url='login')
def delete_contact(request: HttpRequest, *args, **kwargs):
    context = {}

    if request.POST:
        user1 = request.user

        user2_id = kwargs.get('user_id')
        try:
            user2 = Account.objects.get(pk=user2_id)
        except Account.DoesNotExist:
            return HttpResponse(status=404)

        Contact.delete_contact(user1, user2)

        return HttpResponse(json.dumps(context), content_type='application/json')


@login_required(login_url='login')
def accept_request(request: HttpRequest, *args, **kwargs):
    context = {}

    if request.POST:

        sender_id = kwargs.get('user_id')
        try:
            sender = Account.objects.get(pk=sender_id)
        except Account.DoesNotExist:
            return HttpResponse(status=404)

        receiver = request.user

        contact_request = ContactRequest.get_request(sender, receiver)
        if contact_request:
            contact_request.accept()
        else:
            return HttpResponse(status=404)

        return HttpResponse(json.dumps(context), content_type='application/json')


@login_required(login_url='login')
def decline_request(request: HttpRequest, *args, **kwargs):
    context = {}

    if request.POST:

        sender_id = kwargs.get('user_id')
        try:
            sender = Account.objects.get(pk=sender_id)
        except Account.DoesNotExist:
            return HttpResponse(status=404)

        receiver = request.user

        contact_request = ContactRequest.get_request(sender, receiver)
        if contact_request:
            contact_request.decline()
        else:
            return HttpResponse(status=404)

        return HttpResponse(json.dumps(context), content_type='application/json')


@login_required(login_url='login')
def cancel_request(request: HttpRequest, *args, **kwargs):
    context = {}

    if request.POST:
        user1 = request.user

        user2_id = kwargs.get('user_id')
        try:
            user2 = Account.objects.get(pk=user2_id)
        except Account.DoesNotExist:
            return HttpResponse(status=404)

        contact_request = ContactRequest.get_request(user1, user2)
        if contact_request:
            contact_request.decline()
        else:
            return HttpResponse(status=404)

        return HttpResponse(json.dumps(context), content_type='application/json')
