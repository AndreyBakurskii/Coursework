from django.shortcuts import render
from account.models import Account
from contact.models import Contact


def important_people(request):
    context = dict()

    # important_people = []
    #
    # for person in Account.objects.all():
    #     is_friend = False
    #     if Contact.get_contact(request.user, person):
    #         is_friend = True
    #
    #     important_person = {"info": person,
    #                         "is_friend": is_friend,
    #                         }
    #     important_people.append(important_person)

    context['important_people'] = Account.objects.all()

    return render(request, 'important_people/important_people.html', context)
