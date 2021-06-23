import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Contact, ContactRequest
from account.models import Account
from search.utils import user_search


@login_required(login_url='login')
def my_contacts(request: HttpRequest):
    context = {}
    user = request.user
    friends = sorted(Contact.get_friends(user), key=lambda user: user.last_name)

    search_query = request.GET.get("q", default=None)
    if search_query is not None:
        friends = user_search(friends, search_query, is_list=True)

    context['friends'] = friends
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
    FRIENDS, NO_RELATIONSHIP, RECEIVER_REQUEST, SENDER_REQUEST, SELF = range(5)
    context = {}

    if request.POST or from_func:
        user1 = request.user

        user2_id = kwargs.get('user_id')

        context['relationship'] = None

        if user1.id == int(user2_id):
            context['relationship'] = SELF
            return HttpResponse(json.dumps(context), content_type='application/json')

        user2 = None
        try:
            user2 = Account.objects.get(pk=user2_id)
        except Account.DoesNotExist:
            return HttpResponse(status=404)

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
