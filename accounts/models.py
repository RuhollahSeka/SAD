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


def find_overlapped_dateintervals_days(benefactor, start_date, end_date):
    date_diff_days = (end_date - start_date).days
    all_overlapped_days = 0
    useful_dateintervals = []

    for dateinterval in benefactor.dateinterval_set:
        if end_date < dateinterval.begin_date or start_date > dateinterval.end_date:
            continue
        else:
            overlapped_days = (min(end_date, dateinterval.end_date) - max(start_date, dateinterval.begin_date)).days
            all_overlapped_days += overlapped_days
            useful_dateintervals.append((dateinterval.from_json(), overlapped_days))

    for useful_dateinterval in useful_dateintervals:
        useful_dateinterval[1] /= all_overlapped_days

    return useful_dateintervals, all_overlapped_days / date_diff_days


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
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    fax_number = models.CharField(max_length=20)
