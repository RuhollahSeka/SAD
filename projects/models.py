from django.db import models
from accounts.models import *

from django.db import models

from django.db import models
from enum import Enum

import datetime
from django.utils import timezone


# Create your models here.

class Project(models.Model):
    project_name = models.CharField(max_length=200)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, primary_key=False)
    benefactors = models.ManyToManyField(Benefactor, primary_key=False)
    description = models.CharField(max_length=2000)
    project_state = models.CharField(max_length=50)

    def __str__(self):
        return self.project_name


class FinancialProject(Project):
    # TODO set min

    target_money = models.FloatField
    current_money = models.FloatField

    def __str__(self):
        super.__str__(self)


# TODO delete if useless
class NonFinancialProject(Project):

    def __str__(self):
        super.__str__(self)


class AbilityType(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.name


class Ability(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE)
    ability_type = models.ForeignKey(AbilityType, on_delete=models.CASCADE)
    score = models.IntegerField
    description = models.CharField(max_length=300)


class Requirement(models.Model):
    project = models.ForeignKey(NonFinancialProject, on_delete=models.CASCADE, primary_key=False)
    ability_types = models.ManyToManyField(AbilityType, primary_key=False)
    min_age = models.IntegerField
    max_age = models.IntegerField
    gender = models.CharField(max_length=100)
    location = models.CharField(max_length=1000)
    require_quantity = models.IntegerField


class DateInterval(models.Model):
    user = models.OneToOneField(Project, on_delete=models.CASCADE, null=True)
    # TODO can someone pls check what is going on with defining 2 user fields?
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # project
    begin_date = models.DateField
    end_date = models.DateField

    begin_saturday_1 = models.TimeField
    end_saturday_1 = models.TimeField

    begin_sunday_1 = models.TimeField
    end_sunday_1 = models.TimeField

    begin_monday_1 = models.TimeField
    end_monday_1 = models.TimeField

    begin_tuesday_1 = models.TimeField
    end_tuesday_1 = models.TimeField

    begin_wednesday_1 = models.TimeField
    end_wednesday_1 = models.TimeField

    begin_thursday_1 = models.TimeField
    end_thursday_1 = models.TimeField

    begin_friday_1 = models.TimeField
    end_friday_1 = models.TimeField

    begin_saturday_2 = models.TimeField
    end_saturday_2 = models.TimeField

    begin_sunday_2 = models.TimeField
    end_sunday_2 = models.TimeField

    begin_monday_2 = models.TimeField
    end_monday_2 = models.TimeField

    begin_tuesday_2 = models.TimeField
    end_tuesday_2 = models.TimeField

    begin_wednesday_2 = models.TimeField
    end_wednesday_2 = models.TimeField

    begin_thursday_2 = models.TimeField
    end_thursday_2 = models.TimeField

    begin_friday_2 = models.TimeField
    end_friday_2 = models.TimeField


class Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, primary_key=False, related_name='%(class)s_requests_sender')
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, primary_key=False, related_name='%(class)s_requests_receiver')
    description = models.CharField(max_length=2000)


