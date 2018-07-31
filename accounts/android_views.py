from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.generic import TemplateView
from django.template import loader

from projects.models import FinancialProject, NonFinancialProject, Project, Log, Ability
from accounts.models import *

####### Danial imports .Some of them may be redundant!!!

from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from accounts.forms import CharitySignUpForm
from accounts.models import *
from accounts.serializers import *
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def android_user_list(request):
    users = User.objects.all()
    user_serializer = UserSerializer(users, many=True)
    return JsonResponse(user_serializer.data, safe=False)


@csrf_exempt
def android_login(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    password = data.get('password')
    user = User.objects.all().filter(username__iexact=username).filter(password__iexact=password)
    user_serializer = UserSerializer(user, many=True)
    return JsonResponse(user_serializer.data, safe=False)


@csrf_exempt
def android_signup(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    province = data.get('province')
    city = data.get('city')
    address = data.get('address')
    is_benefactor = data.get('is_benefactor')
    is_charity = data.get('is_charity')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    age = data.get('age')
    gender = data.get('gender')

    if User.objects.all().filter(username__iexact=username).count() > 0:
        return JsonResponse('[]', safe=False, status=200)
    contact_info = ContactInfo(country='Iran', province=province, city=city, address=address)
    contact_info.save()

    if is_benefactor:
        user = User(username=username, email=email, password=password, is_benefactor=is_benefactor,
                    is_charity=is_charity)
        user.save()
        benefactor = Benefactor(first_name=first_name, last_name=last_name, age=age, gender=gender, user=user)
        benefactor.save()
    elif is_charity:
        user = User(username=username, email=email, password=password, is_benefactor=is_benefactor,
                    is_charity=is_charity)
        user.save()
        charity = Charity(user=user, name=first_name + last_name)
        charity.save()
    return JsonResponse('[]', safe=False, status=200)
