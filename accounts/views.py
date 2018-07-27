from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader

from projects.models import NonFinancialProject, Project
from accounts.models import *


# Create your views here.

def submit_benefactor_score(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        return HttpResponse([])
    if request.user.is_benefactor:
        # TODO Raise Account Type Error
        return HttpResponse([])
    charity = Charity.objects.get(user=request.user)
    benefactor = Benefactor.objects.get(user=User.objects.get(username=request.POST.get('benefactor_username')))
    if charity.benefactor_history.get(user=benefactor.user) is None:
        # TODO Raise No_Cooperation Error
        return HttpResponse([])
    try:
        ability = AbilityType.objects.get(benefactor=benefactor, name=request.POST.get('ability_type'))
        score = charity.benefactorscore_set.get(benefactor=benefactor, charity=charity)
        if score is None:
            score = BenefactorScore.objects.create(ability_type=ability, benefactor=benefactor,
                                                   charity=Charity.objects.get(user=request.user))
        score.score = int(request.POST.get('score'))
        score.save()
        return HttpResponseRedirect([])
    except:
        return HttpResponse([])
        # TODO raise error


def submit_charity_score(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        return HttpResponse([])
    if request.user.is_charity:
        # TODO Raise Account Type Error
        return HttpResponse([])
    benefactor = Benefactor.objects.get(user=request.user)
    if benefactor.charity_set.get(user=User.objects.get(username=request.POST.get('charity_username'))) is None:
        # TODO Raise No_Cooperation Error
        return HttpResponse([])
    try:
        charity = Charity.objects.get(user=User.objects.get(username=request.POST.get('charity_username')))
        score = benefactor.charityscore_set.get(benefactor=benefactor, charity=charity)
        if score is None:
            score = CharityScore.objects.get(charity=charity, benefactor=Benefactor.objects.get(user=request.user))
        score.score = int(request.POST.get('score'))
        score.save()
        return HttpResponseRedirect([])
    except:
        # TODO raise error
        return HttpResponse([])


def submit_ability_request(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        return HttpResponse([])
    try:
        new_request = AbilityRequest.objects.create(type=request.POST.get('type'), name=request.POST.get('name'),
                                                    description=request.POST.get('description'))
        new_request.save()
        return HttpResponseRedirect([])
    except:
        # TODO Raise Error
        return HttpResponse([])


def submit_cooperation_request(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        return HttpResponse([])
    try:
        if request.user.is_benefactor:
            benefactor = Benefactor.objects.get(user=request.user)
            charity = Charity.objects.get(user=User.objects.get(username=request.POST.get('username')))
            request_type = 'b2c'
        else:
            benefactor = Benefactor.objects.get(user=User.objects.get(username=request.POST.get('username')))
            charity = Charity.objects.get(user=request.user)
            request_type = 'c2b'
        # FIXME How should we find the project? I mean which data is given to find the project with?
        project = NonFinancialProject.objects.get()
        new_request = CooperationRequest.objects.create(benefactor=benefactor, charity=charity, type=request_type,
                                                        description=request.POST.get('description'))
        return HttpResponseRedirect([])
    except:
        # TODO Raise Error
        return HttpResponse('error')
