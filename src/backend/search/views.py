from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from hse.models import Campus, Department, Staff
from account.models import Account


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

    if search_query:
        # проверка на непустой запрос
        search_query = search_query.strip()
        if len(search_query) > 0:
            users = users.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query) |
                                 Q(last_name__icontains=search_query) | Q(first_name__icontains=search_query) |
                                 Q(middle_name__icontains=search_query)
                                 )

    context['users'] = users.order_by('last_name')

    context['campuses'] = Campus.objects.all()
    context['departments'] = Department.objects.all()
    context['staffs'] = Staff.objects.all()

    return render(request, 'search/search.html', context)
