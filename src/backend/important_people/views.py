from django.shortcuts import render
from account.models import Account
from contact.models import Contact
from hse.models import Staff


def important_people(request):
    context = dict()

    edu_staffs = Staff.get_educational_staff()

    context['important_people'] = []
    for edu_staff in edu_staffs:
        context['important_people'].extend(Account.objects.filter(staff=edu_staff))

    return render(request, 'important_people/important_people.html', context)
