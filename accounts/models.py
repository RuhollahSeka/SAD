from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.search_util import *
import datetime, json


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Benefactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=30)

    score = models.FloatField()

    def search_filter(self, min_date_overlap, min_required_hours, min_time_overlap, schedule):
        return has_matched_schedule(min_date_overlap, min_required_hours, min_time_overlap, schedule,
                                    dateinterval_set=self.dateinterval_set)

    def has_ability(self, ability_type_ids, ability_min_score, ability_max_score):
        for ability in self.ability_set.all():
            if ability.ability_type.id in ability_type_ids and ability_min_score < ability.score < ability_max_score:
                return True
        return False


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    grade = models.CharField(max_length=20)

    name = models.CharField(max_length=200)
    score = models.FloatField()
    benefactor_history = models.ManyToManyField(Benefactor, primary_key=False)


class ContactInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(max_length=30, null=True)
    province = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    postal_code = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=500, null=True)
    phone_number = models.CharField(max_length=20, null=True)
