from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    grade = models.CharField(max_length=20)

    name = models.CharField(max_length=200)
    score = models.FloatField()


class Benefactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=30)

    score = models.FloatField()


class ContactInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    fax_number = models.CharField(max_length=20)

