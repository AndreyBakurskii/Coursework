from django.shortcuts import render


def important_people(request):
    return render(request, 'important_people/important_people.html')
