from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.search_util import *
import datetime, json


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    grade = models.CharField(max_length=20)

    name = models.CharField(max_length=200)
    score = models.FloatField()
    benefactor_history = models.ManyToManyField(Benefactor, primary_key=False)


class Benefactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=30)

    score = models.FloatField()

    def search_filter(self, min_date_overlap, min_required_hours, min_time_overlap, schedule):
        wanted_start_date = schedule[0]
        wanted_end_date = schedule[1]
        weekly_schedule = schedule[2]

        (overlapped_dateintervals, overlapped_days) = find_overlapped_dateintervals_days(self, wanted_start_date,
                                                                                         wanted_end_date)

        if overlapped_days < min_date_overlap:
            return False

        overlapped_hours = find_all_overlapped_hours(overlapped_dateintervals, weekly_schedule, min_time_overlap)
        return True if overlapped_hours == max_time(overlapped_hours, min_required_hours) else False


class ContactInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=30)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
