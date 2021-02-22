from django.contrib import admin

from .models import (
    Department,
    Group,
    Campus,
    Staff,
)


class CampusAdmin(admin.ModelAdmin):
    list_display = ('id_campus', 'city')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_educational')


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Staff, StaffAdmin)
