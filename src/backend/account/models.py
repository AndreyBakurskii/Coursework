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
    def create_user(self, email, first_name, middle_name, last_name, password=None, **extra_fields):
        # todo: сделать обработку почты, чтобы оканчивалась на hse.ru
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a firstname')
        if not middle_name:
            raise ValueError('Users must have a middlename')
        if not last_name:
            raise ValueError('Users must have a lastname')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, middle_name, last_name, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            **extra_fields
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
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
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name']

    objects = AccountManager()

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True




