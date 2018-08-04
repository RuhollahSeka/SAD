from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser
from django.views.generic import TemplateView
from django.template import loader
from rest_framework.response import Response

from accounts.log_util import Logger
from accounts.views import get_object, generate_recover_string
from projects.models import FinancialProject, NonFinancialProject, Project, Log
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
from projects.serializers import *
from django.views.decorators.csrf import csrf_exempt
from projects.models import *


@csrf_exempt
@api_view(['POST', 'GET'])
def android_test(request):
    data = {
        'first': 'lol',
        'second': 24
    }

    return Response(data)


@csrf_exempt
def android_user_list(request):
    users = User.objects.all()
    user_serializer = UserSerializer(users, many=True)
    return JsonResponse(user_serializer.data, safe=False)


@csrf_exempt
@api_view(['POST', 'GET'])
def rest_login(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    password = data.get('password')
    tmp_user = User.objects.filter(username=username)
    if len(tmp_user) == 0:
        return Response([])
    tmp_user = get_object(User, username=username)
    if tmp_user.password != password:
        return Response([])
    if not tmp_user.is_active:
        return Response([])
    return Response([{}])


@csrf_exempt
@api_view(['POST', 'GET'])
def rest_username_check(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    if User.objects.filter(username=username).count() > 0:
        return Response({
            'continue': False
        })
    else:
        return Response({
            'continue': True
        })


@csrf_exempt
@api_view(['POST', 'GET'])
def rest_signup(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    province = data.get('province')
    city = data.get('city')
    address = data.get('address')
    phone_number = data.get('phone_number')
    postal_code = data.get('postal_code')
    is_benefactor = data.get('is_benefactor')
    is_charity = data.get('is_charity')
    description = data.get('description')

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    age = data.get('age')
    gender = data.get('gender')

    charity_name = data.get('charity_name')

    user = User.objects.all().filter(username__iexact=username)

    if user.count() > 0:
        return Response({
            'success': False
        })
    contact_info = ContactInfo(country='Iran', province=province, city=city, address=address, phone_number=phone_number,
                               postal_code=postal_code)
    contact_info.save()

    if is_benefactor:
        user = User(username=username, email=email, password=password, is_benefactor=is_benefactor,
                    description=description, is_charity=is_charity)
        user.save()
        benefactor = Benefactor(first_name=first_name, last_name=last_name, age=age, gender=gender, user=user)
        benefactor.save()
    elif is_charity:
        user = User(username=username, email=email, password=password, is_benefactor=is_benefactor,
                    is_charity=is_charity)
        user.save()
        charity = Charity(user=user, name=charity_name)
        charity.save()
    code = generate_recover_string()
    message = 'برای فعال شدن حساب خود بر روی لینک زیر کلیک کنید:' + '\n'
    message += 'http://127.0.0.1:8000/' + 'activate/' + str(user.id) + '/' + code
    user.activation_string = code
    user.save()
    email_message = EmailMessage('Activation Email', message, to=[user.email])
    email_message.send()
    return Response({
        'success': True
    })


@csrf_exempt
def rest_financial_project_search(request):
    data = JSONParser().parse(request)
    project_name = data.get('proj_name')
    charity_name = data.get('inst_name')
    min_progress = data.get('min_progress')
    max_progress = data.get('max_progress')
    min_deadline_date = data.get('min_deadline')
    max_deadline_date = data.get('max_deadline')
    # TODO search for non finished projects
    project_queryset = search_financial_project(project_name=project_name, charity_name=charity_name,
                                                min_progress=min_progress, max_progress=max_progress,
                                                min_deadline_date=min_deadline_date, max_deadline_date=max_deadline_date)
    result_serializer = FinancialProjectSerializer(project_queryset, many=True)
    return JsonResponse(result_serializer.data, safe=False)


@csrf_exempt
def rest_non_financial_projects_search(request):
    if not request.user.is_authenticated:
        return Response({
            'success': False
        })
    # if request.user.is_charity:
    #     # TODO Raise Account Type Error
    #     context = error_context_generate('Account Type Error', 'Charities Cannot Search for Projects', '')
    #     template = loader.get_template(reverse('accounts:error_page'))
    #     return HttpResponse(template.render(context, request))
    all_ability_types = [ability_type.name for ability_type in AbilityType.objects.all()]
    all_ability_tags = [ability_tag.name for ability_tag in AbilityTag.objects.all()]

    if request.method == 'GET':
        return Response({

        })
    data = JSONParser().parse(request)

    project_name = data.get('search_non_financial_project_name')
    charity_name = data.get('search_non_financial_charity_name')
    project_state = data.get('search_non_financial_project_state')
    ability_name = data.get('search_non_financial_ability_name')
    tags = data.get('search_non_financial_tags')
    project_queryset = search_non_financial_project(project_name=project_name, charity_name=charity_name,
                                                    project_state=project_state, ability_name=ability_name, tags=tags)
    result_serializer = NonFinancialProjectSerializer(project_queryset, many=True)
    return JsonResponse(result_serializer.data, safe=False)


@csrf_exempt
@api_view(['POST', 'GET'])
def rest_user_projects(request):
    data = JSONParser().parse(request)
    username = data.get('username')
    benefactor = User.objects.filter(username__iexact=username)[0].benefactor
    projects = []
    for project in benefactor.project_set:
        projects.append({
            'proj_name': project.project_name,
            'state': project.project_state,
            'description': project.description
        })
    return Response(projects)


@csrf_exempt
@api_view(['POST', 'GET'])
def rest_user_profile(request):
    # TODO check security stuff

    data = JSONParser().parse(request)
    given_username = data.get('username')
    user = User.objects.filter(username__iexact=given_username)[0]

    return Response({
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'province': user.contact_info.province,
        'city': user.contact_info.city,
        'address': user.contact_info.address,
        'is_benefactor': user.is_benefactor,
        'is_charity': user.is_charity,
        'first_name': user.benefactor.first_name if user.is_benefactor else user.charity.name,
        'last_name': user.benefactor.last_name if user.is_benefactor else None,
        'age': user.benefactor.age if user.is_benefactor else None,
        'gender': user.benefactor.gender if user.is_benefactor else None
    })


@csrf_exempt
@api_view(['POST', 'GET'])
def rest_get_tags(request):
    tags = [tag.name for tag in AbilityTag.objects.all()]
    return Response(tags)
