from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'staff', 'department', 'group', 'last_login', 'is_admin')
    search_fields = ('email', 'first_name', 'middle_name', 'last_name', 'department')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    ordering = ('email',)


admin.site.register(Account, AccountAdmin)
