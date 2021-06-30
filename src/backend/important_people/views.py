from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from account.models import Account
from hse.models import Staff
from search.utils import user_search


@login_required(login_url='login')
def important_people(request):
    context = dict()

    edu_staffs = Staff.get_educational_staff()
    context['important_people'] = Account.objects.filter(staff__in=edu_staffs)

    search_query = request.GET.get("q")
    context['important_people'] = user_search(context['important_people'], search_query, is_query_set=True)

    return render(request, 'important_people/important_people.html', context)
