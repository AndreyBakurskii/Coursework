import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Contact, ContactRequest
from account.models import Account
# Create your views here.


# def my_requests(request: HttpRequest):
#     context = {}
#     user = request.user
#
#     if request.POST:
#         sender_id = request.POST['sender_id']
#         sender = Account.objects.get(pk=sender_id)
#
#         # context['answer'] = 'Лови ответ от сервака!'
#         print(sender_id)
#         request_contact = ContactRequest.get_request(sender, user)
#         print(request_contact)
#
#         if request.POST['decision'] == 'accept':
#             request_contact.accept()
#
#         elif request.POST['decision'] == 'decline':
#             request_contact.decline()
#
#         return HttpResponse(status=200)
#         # return HttpResponse(json.dumps(context), content_type='application/json')
#
#     else:
#         context['senders'] = ContactRequest.get_senders(user)
#
#         return render(request, 'contact/my_requests.html', context)


def my_contacts(request: HttpRequest):
    context = {}
    user = request.user

    if request.GET.get('q'):
        context['friends'] = Contact.get_friends(user)


    context['senders_requests'] = ContactRequest.get_senders(user)

    # context['friends'] = Account.objects.all().order_by('last_name')
    return render(request, 'contact/contacts.html', context)


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
        print(type(request.POST))
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
    pass
