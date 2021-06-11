from django.db.models import Q


def user_search(users, search_query: str, is_query_set=False, is_list=False):
    if search_query:
        # проверка на непустой запрос
        search_query = search_query.strip()
        if len(search_query) > 0:
            for word in search_query.split():
                if is_query_set:
                    users = users.filter(Q(username__icontains=word) | Q(email__icontains=word) |
                                         Q(last_name__icontains=word) | Q(first_name__icontains=word) |
                                         Q(middle_name__icontains=word)
                                         )
                elif is_list:
                    users = [user for user in users
                             if f'{user.last_name} {user.first_name} {user.middle_name} {user.email}' \
                             f' {user.username}'.find(search_query) != -1]
    return users
