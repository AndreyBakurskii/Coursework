from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from hse.models import Campus, Department, Staff
from account.models import Account
from .utils import user_search


@login_required(login_url='login')
def search(request: HttpRequest):
    context = {}

    campus_id = request.GET.get('campus', default=None)
    department_id = request.GET.get('department', default=None)
    staff_id = request.GET.get('staff', default=None)

    search_query = request.GET.get("q", default=None)

    users = Account.objects.all()
    if campus_id:
        try:
            campus = Campus.objects.get(id_campus=campus_id)
        except Campus.DoesNotExist:
            return HttpResponse(status=404)

        users = users.filter(campus=campus)

    if department_id:
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            return HttpResponse(status=404)

        users = users.filter(department=department)

    if staff_id:
        try:
            staff = Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            return HttpResponse(status=404)

        users = users.filter(staff=staff)

    users = user_search(users, search_query, is_query_set=True)

    context['users'] = users

    context['campuses'] = Campus.objects.all()
    context['departments'] = Department.objects.all()
    context['staffs'] = Staff.objects.all()

    return render(request, 'search/search.html', context)


