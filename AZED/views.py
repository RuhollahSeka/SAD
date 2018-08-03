from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from accounts.forms import CharitySignUpForm
from accounts.models import *

###Home
from projects.models import Project, FinancialProject, CooperationRequest, FinancialContribution, Log
from projects.views import error_context_generate, get_object


def handle_admin_security(request):
    user = request.user
    if not user.is_authenticated:
        context = error_context_generate('Authentication Error', 'لطفاً اول وارد شوید', 'accounts:login_view')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', 'Home')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not user.is_admin:
        context = error_context_generate('Account Type Error',
                                         'Only Admins can Access This Page', 'Home')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


class HomeView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['login'] = True
            context['username'] = self.request.user.username
        else:
            context['login'] = False

        return context


###Error

class ErrorView(TemplateView):
    template_name = "error_page.html"


def error_redirect(request, redirect_address):
    return HttpResponseRedirect(reverse(redirect_address))


def index(request):
    return render(request, 'accounts/index.html')


def contact(request):
    return render(request, 'accounts/contact.html')


def about(request):
    return render(request, 'accounts/about.html')


def admin_get_request_related_stuff(request):
    all_ability_requests = AbilityRequest.objects.all()
    all_cooperation_requests = CooperationRequest.objects.all()
    all_notifications = Notification.objects.all()
    all_logs = Log.objects.all()
    # FIXME fix url
    return render(request, 'url', {
        'all_ability_requests': all_ability_requests,
        'all_cooperation_requests': all_cooperation_requests,
        'all_notifications': all_notifications,
        'all_logs': all_logs
    })


def admin_get_charities(request):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    try:
        charities = Charity.objects.all()
        charity_update_logs = {log for log in Log.objects.all() if
                               log.first_actor.is_charity and log.log_type is 'account_update'}
        # FIXME fix url
        context = {
            'all_charities': list(charities),
            'update_logs': list(charity_update_logs),
        }
        template = loader.get_template('path-to-template')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', 'Home')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_get_benefactors(request):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    try:
        benefactors = Benefactor.objects.all()
        benefactor_update_logs = {log for log in Log.objects.all() if
                                  log.first_actor.is_benefactor and log.log_type is 'account_update'}
        # FIXME fix url
        context = {
            'all_benefactors': list(benefactors),
            'update_logs': list(benefactor_update_logs),
        }
        template = loader.get_template('path-to-template')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', 'Home')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_get_tags(request):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    try:
        tags = AbilityTag.objects.all()
        context = {'tags': tags}
        template = loader.get_template('path-to-template')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', 'Home')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_first_page_data(request):
    benefactor_len = len(Benefactor.objects.all())
    charity_len = len(Charity.objects.all())
    project_len = len(Project.objects.all())
    all_money_spent = 0
    for financial_project in FinancialProject.objects.all():
        all_money_spent += financial_project.current_money
    # FIXME fix url
    return render(request, 'url', {
        'benefactor_len': benefactor_len,
        'charity_len': charity_len,
        'project_len': project_len,
        'all_money_spent': all_money_spent
    })


def admin_dashboard(request):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    try:
        charity_count = Charity.objects.all().count()
        benefactor_count = Benefactor.objects.all().count()
        project_count = Project.objects.all().count()
        contributions_sum = 0
        for cont in FinancialContribution.objects.all():
            contributions_sum += cont.money
        tag_count = AbilityTag.objects.all().count()
        ability_type_count = AbilityType.objects.count()
        score_count = BenefactorScore.objects.count()
        score_count += CharityScore.objects.count()
        comment_count = BenefactorComment.objects.count()
        comment_count += CharityComment.objects.count()
        inactive_users = User.objects.filter(is_active=False).all()
        context = {
            'charity_count': charity_count,
            'benefactor_count': benefactor_count,
            'project_count': project_count,
            'contributions_sum': contributions_sum,
            'tag_count': tag_count,
            'ability_type_count': ability_type_count,
            'score_count': score_count,
            'comment_count': comment_count,
            'inactive_users': inactive_users
        }
        # TODO Fix template path and Redirect
        template = loader.get_template('path-to-template')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', 'Home')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def deactivate_user(request, uid):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    try:
        user = get_object(User, id=uid)
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse(''))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', '')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def activate_user(request, uid):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    try:
        user = get_object(User, id=uid)
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse(''))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', '')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))