# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend
#
#
# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, email=None, **kwargs):
#         Account = get_user_model()
#         if username:
#             try:
#                 user = Account.objects.get(username=username)
#             except Account.DoesNotExist:
#                 return None
#             else:
#                 if user.check_password(password):
#                     return user
#         elif email:
#             try:
#                 user = Account.objects.get(email=email)
#             except Account.DoesNotExist:
#                 return None
#             else:
#                 if user.check_password(password):
#                     return user
#
#         return None
