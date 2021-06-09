from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from hse.models import Campus, Department, Group, Staff
from account.models import Account


def search(request: HttpRequest):
    context = {}

    campus_id = request.GET.get('campus', default=None)
    department_id = request.GET.get('department', default=None)
    staff_id = request.GET.get('staff', default=None)

    users = Account.objects.all()
    if campus_id:
        try:
            campus = Campus.objects.get(id_campus=campus_id)
        except Campus.DoesNotExist:
            return HttpResponse(status=404)

        users.filter(campus=campus)

    if department_id:
        try:
            department = Department.objects.get(pk=department_id)
        except Campus.DoesNotExist:
            return HttpResponse(status=404)

        users.filter(department=department)

    if staff_id:
        try:
            staff = Staff.objects.get(pk=staff_id)
        except Campus.DoesNotExist:
            return HttpResponse(status=404)

        users.filter(staff=staff)

    context['users'] = users
    return render(request, 'search/search.html', context)
