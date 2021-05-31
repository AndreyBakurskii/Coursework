from django.shortcuts import render


def index(request):
    return render(request, 'search/search.html')

# Create your views here.
