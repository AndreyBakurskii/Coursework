from django.db import models

from datetime import datetime


# Номера кампусов:
# 22726  - Москва
# 135288 - Нижний Новгород
# 135083 - Санкт-Петербург
# 135213 - Пермь
class Campus(models.Model):
    id_campus = models.CharField(primary_key=True, verbose_name="id_campus", max_length=10, blank=False, unique=True)
    city = models.CharField(primary_key=False, verbose_name="city_campus", max_length=50, blank=False, unique=True)

    class Meta:
        verbose_name_plural = 'Campuses'

    def __str__(self):
        return f"{self.city}"


class Department(models.Model):
    name = models.CharField(verbose_name="name_dept", max_length=50, null=False, blank=False)
    full_name = models.CharField(verbose_name="full_name_dept", max_length=255, null=False, blank=False)
    campus = models.ForeignKey(Campus, verbose_name="campus_dept", on_delete=models.CASCADE, blank=False)

    class Meta:
        constraints = [
                models.UniqueConstraint(fields=['name', 'campus'], name='unique_department'),
                ]

    def __str__(self):
        return f"{self.name} ({self.campus.city})"


class Group(models.Model):
    name = models.CharField(verbose_name="name_group", max_length=50, null=False, blank=False)
    start_year = models.DateField(verbose_name="start_year", default=datetime(year=2019, month=8, day=30))
    graduate_year = models.DateField(verbose_name="finish_year", default=datetime(year=2023, month=7, day=30))
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="department")

    class Meta:
        constraints = [
                models.UniqueConstraint(fields=['name', 'department'], name='unique_group'),
                ]

    def __str__(self):
        return f"{self.name}"


class Staff(models.Model):
    name = models.CharField(verbose_name="name_staff", max_length=50, null=False, blank=False, unique=True)
    is_educational = models.BooleanField(verbose_name="is_educational", blank=False)

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def get_educational_staff():
        return Staff.objects.filter(is_educational=True)
