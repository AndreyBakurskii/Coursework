import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import Contact, ContactRequest
from account.models import Account
# Create your views here.


def show_request(request: HttpRequest):
    return render(request, 'contact/request.html')


def request(request: HttpRequest):
    pass


def my_requests(request: HttpRequest):
    context = {}
    user = request.user

    if request.POST:
        sender_id = request.POST['sender_id']
        sender = Account.objects.get(pk=sender_id)

        # context['answer'] = 'Лови ответ от сервака!'
        print(sender_id)
        request_contact = ContactRequest.get_request(sender, user)
        print(request_contact)

        if request.POST['decision'] == 'accept':
            request_contact.accept()

        elif request.POST['decision'] == 'decline':
            request_contact.decline()

        return HttpResponse(status=200)
        # return HttpResponse(json.dumps(context), content_type='application/json')

    else:
        context['senders'] = ContactRequest.get_senders(user)

        return render(request, 'contact/my_requests.html', context)


def my_contacts(request: HttpRequest):
    context = {}
    user = request.user

    # context['friends'] = Contact.get_friends(user)

    context['friends'] = Account.objects.all()
    return render(request, 'account/base2.html', context)


def important_people(request: HttpRequest):
    context = {}
    return render(request, 'contact/important_people.html')


def thx(request: HttpRequest):
    return render(request, 'contact/thx.html')
