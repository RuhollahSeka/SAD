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


def android_user_list(request):
    users = User.objects.all()
    user_serializer = UserSerializer(users, many=True)
    return JsonResponse(user_serializer.data, safe=False)


def android_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User.objects.all().filter(username__iexact=username).filter(password__iexact=password)
    user_serializer = UserSerializer(user)
    return JsonResponse(user_serializer, safe=False)
