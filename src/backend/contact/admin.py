from django.contrib import admin
from .models import Contact, ContactRequest
# Register your models here.


class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'is_active')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2')


admin.site.register(ContactRequest, ContactRequestAdmin)
admin.site.register(Contact, ContactAdmin)
