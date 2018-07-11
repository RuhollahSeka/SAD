from django.db import models
from accounts.models import *

from django.db import models

from django.db import models
from enum import Enum

import datetime
from django.utils import timezone


# Create your models here.

class DateInterval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # project
    begin = models.DateField
    end = models.DateField


class Weekday(models.Model):
    date_interval = models.ForeignKey(DateInterval, on_delete=models.CASCADE, primary_key=False)
    day_name = models.CharField(max_length=50)


class HourInterval(models.Model):
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE, primary_key=False)
    begin = models.TimeField()
    end = models.TimeField()


class Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, primary_key=False)
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, primary_key=False)
    description = models.CharField(max_length=2000)


class AbilityType(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    pass


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, primary_key=False)
    benefactors = models.ManyToManyField(Benefactor, on_delete=models.DO_NOTHING, primary_key=False)
    description = models.CharField(max_length=2000)
    project_state = models.CharField(max_length=50)


class FinancialProject(Project):
    # TODO set min

    target_money = models.FloatField()
    current_money = models.FloatField()


# TODO delete if useless
class NonFinancialProject(Project):
    pass


class Requirement(models.Model):
    project = models.ForeignKey(NonFinancialProject, on_delete=models.CASCADE, primary_key=False)
    ability_types = models.ManyToManyField(AbilityType, models.DO_NOTHING, primary_key=False)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    gender = models.CharField(max_length=100)
    location = models.CharField(max_length=1000)
    require_quantity = models.IntegerField()
