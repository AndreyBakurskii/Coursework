from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request: HttpRequest):
    return redirect('messenger')
