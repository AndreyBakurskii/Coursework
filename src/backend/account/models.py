from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)

from hse.models import (
    Campus,
    Department,
    Group,
    Staff,
)


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if email:
            if not email.endswith("hse.ru"):
                raise ValueError('User`s email must end with "hse.ru"')
        else:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(verbose_name="username", max_length=50, unique=True)
    email = models.EmailField(verbose_name="email", max_length=50, unique=True)

    first_name = models.CharField(verbose_name="first_name", max_length=40)
    middle_name = models.CharField(verbose_name="middle_name", max_length=40)
    last_name = models.CharField(verbose_name="last_name", max_length=40)

    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="campus", default=None)

    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name="staff", default=None)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name="department", default=None)

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name="group", default=None)

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    class Meta:
        ordering = ['last_name']

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
