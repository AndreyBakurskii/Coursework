"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .views import (registration_fio,
                    registration_campus,
                    registration_choose_staff,
                    registration_ed_staff,
                    registration_staff,
                    registration_department,
                    registration_group,
                    registration_end,
                    login_view, thanks_page, logout_view,
                    account_view,
                    # test_add_campus
                    )


urlpatterns = [
    path('registration/fio', registration_fio, name='reg_fio'),
    path('registration/campus', registration_campus, name='reg_campus'),
    path('registration/staff', registration_staff, name='reg_staff'),
    path('registration/choose_staff', registration_choose_staff, name='reg_choose_staff'),
    path('registration/ed_staff', registration_ed_staff, name='reg_ed_staff'),
    path('registration/department', registration_department, name='reg_department'),
    path('registration/group', registration_group, name='reg_group'),
    path('registration/end', registration_end, name='reg_end'),
    path('logout', logout_view, name='logout'),
    path('login', login_view, name='login'),
    path('thanks', thanks_page, name='thanks_page'),
    path('<user_id>', account_view, name='account_view')
    # path('testing', test_add_campus, name='testing_page'),

]
