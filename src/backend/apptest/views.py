from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse

from django import forms


def home(request: HttpRequest):
    context = {}

    if not request.user.is_authenticated:
        return redirect('account/login')

    context['user'] = request.user
    return render(request, 'apptest/home.html', context=context)


# !!!! поиск аккаунтов !!!!
# from django.db.models import Q
#
#
# def account_search_view(request):
#     context = {}
#     if request.method == "GET":
#         search_query = request.GET.get("q")
#         if len(search_query) > 0:
#
#             search_results = Account.objects.filter(
#                 Q(username__icontains=search_query) | Q(email__icontains=search_query)
#             )
#             context['search_results'] = search_results
#
#             #### связь с контактами ####
#             # user = request.user
#             # accounts = []  # [(account1, True), (account2, False), ...]
#             # if user.is_authenticated:
#             #     # get the authenticated users friend list
#             #     auth_user_friend_list = FriendList.objects.get(user=user)
#             #     for account in search_results:
#             #         accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
#             #     context['accounts'] = accounts
#             # else:
#             #     for account in search_results:
#             #         accounts.append((account, False))
#             #     context['accounts'] = accounts
#
#     return render(request, "account/search.html", context)
