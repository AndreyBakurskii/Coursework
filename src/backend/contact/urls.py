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
from django.urls import path, include
from .views import (my_contacts,
                    accept_request,
                    decline_request,
                    delete_contact,
                    cancel_request,
                    define_relationship,
                    create_contact
                    )

urlpatterns = [
    path('my_contacts', my_contacts, name='my_contacts'),
    path('accept_request_from_user/<user_id>', accept_request),
    path('decline_request_from_user/<user_id>', decline_request),
    path('cancel_request_to_user/<user_id>', cancel_request),
    path('delete_contact_with_user/<user_id>', delete_contact),
    path('define_relationship_with_user/<user_id>', define_relationship),
    path('create_contact_with_user/<user_id>', create_contact),
]
