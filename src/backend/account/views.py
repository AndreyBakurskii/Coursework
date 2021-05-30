from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, RegistrationFIOEmailForm, RegistrationEndForm, LoginForm
from hse.models import Campus, Department, Group, Staff
from account.models import Account


def registration_fio(request):
    context = dict()

    if request.POST:
        form = RegistrationFIOEmailForm(request.POST)
        if form.is_valid():
            request.session['email'] = form.cleaned_data.get('email').lower()
            request.session['first_name'] = form.cleaned_data.get('first_name')
            request.session['middle_name'] = form.cleaned_data.get('middle_name')
            request.session['last_name'] = form.cleaned_data.get('last_name')

            return redirect('reg_campus')
    else:
        form = RegistrationFIOEmailForm()

    context['reg_fio_form'] = form
    return render(request, 'account/reg_fio_email.html', context)


def registration_campus(request):
    context = dict()

    if request.POST:
        if request.POST['action'] == 'next':
            request.session['campus'] = request.POST['group1']
            return redirect('reg_staff')

        else:
            return redirect('reg_fio')

    return render(request, 'account/reg_campus.html', context)


def registration_staff(request):
    context = dict()
    if request.POST:
        print(request.session['campus'])

        if request.POST['action'] == 'next':

            request.session['student'] = False
            request.session['employee'] = False

            if request.POST['group2'] == 'student':
                request.session['student'] = True
                return redirect('reg_department')
            else:
                request.session['employee'] = True
                return redirect('reg_ed_staff')
        else:
            return redirect('reg_campus')

    return render(request, 'account/reg_staff.html', context)


def registration_department(request):
    context = dict()
    context['errors'] = []

    if request.POST:
        if request.POST['action'] == 'next':
            if request.POST['department']:
                request.session['department'] = request.POST['department']

                if request.session['student']:
                    return redirect('reg_group')
                else:
                    return redirect('reg_choose_staff')
            else:
                context['errors'].append("Выберите факультет, на котором вы обучаетесь или работаете!")
        else:
            if request.session['student']:
                return redirect('reg_staff')
            else:
                return redirect('reg_ed_staff')

    else:
        campus = Campus.objects.get(city=request.session['campus'])
        context['departments'] = Department.objects.all().filter(campus=campus)

    return render(request, 'account/reg_department.html', context)


def registration_ed_staff(request):
    context = dict()

    if request.POST:

        if request.POST['action'] == 'next':

            if request.POST['group2'] == 'edu':
                request.session['educational_employee'] = True
                return redirect('reg_department')
            else:
                request.session['educational_employee'] = False
                return redirect('reg_choose_staff')

        else:
            return redirect('reg_staff')

    return render(request, 'account/reg_ed_staff.html', context)


def registration_choose_staff(request):
    context = dict()
    context['errors'] = []

    if request.POST:

        if request.POST['action'] == 'next':
            if request.POST['staff']:
                request.session['staff'] = request.POST['staff']
                return redirect('reg_end')
            else:
                context['errors'].append("Выберите должность, которую Вы занимаете!")

        else:
            if request.session['educational_employee']:
                return redirect('reg_department')

            return redirect('reg_ed_staff')

    else:
        context['staffs'] = Staff.objects.all().filter(is_educational=request.session['educational_employee'])

    return render(request, 'account/reg_choose_staff.html', context)


def registration_group(request):
    context = dict()
    context['errors'] = []

    if request.POST:

        if request.POST['action'] == 'next':
            if request.POST['group']:
                request.session['group'] = request.POST['group']
                return redirect('reg_end')
            else:
                context['errors'].append("Выберите группу, в которой Вы учитесь!")
        else:
            return redirect('reg_department')

    else:
        campus = Campus.objects.get(city=request.session['campus'])
        department = Department.objects.get(name=request.session['department'], campus=campus)

        context['groups'] = Group.objects.all().filter(department=department)

    return render(request, 'account/reg_group.html', context)


def registration_end(request):
    context = dict()

    context['errors'] = []

    if request.POST:

        if request.POST['action'] == 'end':

            form = RegistrationEndForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password1 = request.POST['password1']

                email = request.session['email']

                new_user = Account.objects.create_user(email=email, username=username, password=password1)

                new_user.first_name = request.session['first_name']
                new_user.middle_name = request.session['middle_name']
                new_user.last_name = request.session['last_name']

                new_user.campus = Campus.objects.get(city=request.session['campus'])

                # получаем все данные из session
                if request.session['student']:
                    new_user.department = Department.objects.get(name=request.session['department'])
                    new_user.group = Group.objects.get(name=request.session['group'])

                else:
                    if request.session['educational_employee']:
                        new_user.department = Department.objects.get(name=request.session['department'])

                    new_user.staff = Staff.objects.get(name=request.session['staff'])

                new_user.save()

                user = authenticate(request, username=email, password=password1)
                if user:
                    login(request, user)
                    return redirect("home")
        else:
            if request.session['student']:
                return redirect('reg_group')

            return redirect('reg_choose_staff')

    else:
        form = RegistrationEndForm()

    context['reg_end_form'] = form

    return render(request, 'account/reg_end.html', context)


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            # параметру username передаем email, при аутентификации проверяется поле user_model.USERNAME_FIELD, а оно
            # соответсвует полю user_model.email
            user = authenticate(request, username=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = LoginForm()

    context['login_form'] = form
    print(form.errors)

    return render(request, "account/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


def account_view(request, *args, **kwargs):
    context = {}

    user_id = kwargs.get('user_id')

    try:
        user = Account.objects.get(pk=user_id)
    except:
        return HttpResponse('Something went wrong')

    context['fio'] = " ".join([user.first_name, user.middle_name, user.last_name])
    context['username'] = user.username
    context['email'] = user.email

    return render(request, "account/account_view.html", context)


def thanks_page(request):
    print("hello")
    return render(request, 'account/base3.html')
