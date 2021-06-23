from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from account.models import Account


class RegistrationUserFromAdminSite(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'middle_name', 'last_name', 'campus', 'staff', 'department',
                  'group', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']

        # проверка на принадлежность почты к ВШЭ
        if not email.endswith("hse.ru"):
            raise forms.ValidationError('Почта должна быть корпоративной, оканчиваться на "hse.ru"')

        # проверка на существование зарегистрированного пользователя с такой же почтой
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f'Пользователь с этой почтой "{email}" уже зарегистрирован')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f'Пользователь с этом никнеймом "{username}" уже зарегистрирован')


class AccountAdmin(UserAdmin):
    add_form = RegistrationUserFromAdminSite

    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'campus', 'staff', 'department', 'group',
                    'last_login', 'is_admin')

    search_fields = ('email', 'username', 'first_name', 'middle_name', 'last_name', 'department')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 'campus', 'staff', 'department', 'group')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'middle_name', 'last_name', 'campus', 'staff', 'department',
                       'group', 'password1', 'password2')}
         ),
    )

    ordering = ('email',)


# admin.site.unregister(Account)
admin.site.register(Account, AccountAdmin)
