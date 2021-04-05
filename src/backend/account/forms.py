from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account

from hse.models import *


class RegistrationForm(UserCreationForm):
    pass


class RegistrationFIOEmailForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'middle_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if not email.endswith("hse.ru"):
            raise forms.ValidationError("Email должен оканчиваться на hse.ru")

        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)

        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Этот email уже используется, введите другой.')


class RegistrationEndForm(forms.Form):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f'Пользователь с этим никнеймом "{username}" уже зарегистрирован')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")

        return password2


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email',)

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            if not email.endswith("hse.ru"):
                raise forms.ValidationError("Email должен оканчиваться на hse.ru")

            password = self.cleaned_data['password']
            # print(email, password)
            # параметру username передаем email, при аутентификации проверяется поле user_model.USERNAME_FIELD, а оно
            # соответсвует полю user_model.email
            if not authenticate(username=email, password=password):
                raise forms.ValidationError("Неверная почта или пароль!")
