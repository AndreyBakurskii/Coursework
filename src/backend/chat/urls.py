from django.urls import path

from .views import messenger

urlpatterns = [
    path('', messenger, name='messenger'),
]
