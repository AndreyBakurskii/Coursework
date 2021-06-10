from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from account.models import Account
from hse.models import Staff


@login_required(login_url='login')
def important_people(request):
    context = dict()

    edu_staffs = Staff.get_educational_staff()
    context['important_people'] = Account.objects.filter(staff__in=edu_staffs)

    search_query = request.GET.get("q")
    # проверка на None
    if search_query:
        # проверка на непустой запрос
        search_query = search_query.strip()
        if len(search_query) > 0:
            context['important_people'] = context['important_people'].filter(
                Q(username__icontains=search_query) | Q(email__icontains=search_query) |
                Q(last_name__icontains=search_query) | Q(first_name__icontains=search_query) |
                Q(middle_name__icontains=search_query)
            )

    return render(request, 'important_people/important_people.html', context)
