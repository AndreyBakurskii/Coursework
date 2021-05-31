from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest):
    context = {}

    if not request.user.is_authenticated:
        return redirect('account/login')

    context['user'] = request.user
    return render(request, 'website/home.html', context=context)
