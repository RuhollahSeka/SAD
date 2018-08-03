from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from accounts.forms import CharitySignUpForm
from accounts.log_util import Logger
from accounts.models import *

###Home
from projects.models import Project, FinancialProject, CooperationRequest, FinancialContribution, Log, \
    NonFinancialProject, DateInterval
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


def add_request(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    data = request.POST
    request_type = data.get('request_type')
    state = data.get('request_state')
    benefactor_id = data.get('benefactor_id')
    charity_id = data.get('charity_id')
    project_id = data.get('project_id')
    description = data.get('description')

    benefactor_user = get_object(User, id=benefactor_id)
    charity_user = get_object(User, id=charity_id)
    project = get_object(Project, id=project_id)
    if benefactor_user is None or charity_user is None or project is None:
        # TODO error
        pass

    cooperation_request = CooperationRequest(type=request_type, state=state, benefactor=benefactor_user.benefactor,
                                             charity=charity_user.charity, project=project, description=description)
    cooperation_request.save()
    # TODO add request


def edit_request(request, rid):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure

    cooperation_request = get_object(CooperationRequest, id=rid)
    if cooperation_request is None:
        # TODO some error
        pass
    if request.method == 'GET':
        # TODO url?
        return render(request, 'url', {
            'request_type': cooperation_request.type,
            'benefactor_id': cooperation_request.benefactor.user.id,
            'charity_id': cooperation_request.charity.user.id,
            'project_id': cooperation_request.project.id,
            'description': cooperation_request.description
        })
    elif request.method == 'POST':
        data = request.POST
        benefactor_id = data.get('benefactor_id')
        charity_id = data.get('charity_id')
        project_id = data.get('project_id')
        benefactor_user = get_object(User, id=benefactor_id)
        charity_user = get_object(User, id=charity_id)
        project = get_object(Project, id=project_id)
        if benefactor_user is None or charity_user is None or project is None:
            # TODO error
            pass
        cooperation_request.type = data.get('type')
        cooperation_request.benefactor = benefactor_user.benefactor
        cooperation_request.charity = benefactor_user.charity
        cooperation_request.project = project
        cooperation_request.description = data.get('description')
        cooperation_request.save()
        # TODO url?
        return render(request, 'url', {})
    # TODO do something?


def delete_cooperation_request(request, rid):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    cooperation_request = get_object(CooperationRequest, id=rid)
    if cooperation_request is None:
        # TODO error
        pass
    cooperation_request.delete()
    # TODO delete success


def delete_ability_request(request, rid):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    ability_request = get_object(AbilityRequest, id=rid)
    if ability_request is None:
        # TODO error
        pass
    ability_request.delete()
    # TODO delete success


def add_new_admin(request):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    data = request.POST
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    # try:
    contact_info = ContactInfo()
    contact_info.save()
    new_admin = User(is_admin=True, is_active=True, admin_approved=True, username=username, password=password,
                     contact_info=contact_info, email=email)
    new_admin.save()
    mail = EmailMessage('Admin Promotion', 'شما به عنوان ادمین سایت مرساد انتخاب شدید.', to=[email])
    mail.send()
    return HttpResponseRedirect(reverse('admin'))
    # except:
    #     context = error_context_generate('Add Error',
    #                                      'اضافه کردن ادمین با مشکل روبرو شد!', 'admin')
    #     template = loader.get_template('accounts/error_page.html')
    #     return HttpResponse(template.render(context, request))


def create_project(charity, type, project_name='my project', description='this is my project', project_state='open'):
    project = Project(charity=charity, type=type, project_name=project_name, description=description,
                      project_state=project_state)
    project.save()
    return project


def add_non_financial_project(request):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    data = request.POST
    project_name = data.get('project_name')
    description = data.get('description')
    project_state = data.get('project_state')
    charity_id = data.get('charity_id')
    charity_user = get_object(User, id=charity_id)
    if charity_user is None:
        # TODO some error
        pass
    try:
        ability_type_id = data.get('ability_type_id')
        ability_type = get_object(AbilityType, id=ability_type_id)
        if ability_type is None:
            # TODO some error
            pass
        project = create_project(charity_user.charity, 'non-financial', project_name, description, project_state)
        min_age = data.get('min_age')
        max_age = data.get('max_age')
        required_gender = data.get('required_gender')
        country = data.get('country')
        province = data.get('province')
        city = data.get('city')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        schedule = data.get('schedule')
        non_financial_project = NonFinancialProject(project=project, ability_type=ability_type, min_age=min_age,
                                                    max_age=max_age, required_gender=required_gender, country=country,
                                                    province=province, city=city)
        non_financial_project.save()
        dateinterval = DateInterval(begin_date=start_date, end_date=end_date,
                                    non_financial_project=non_financial_project)
        dateinterval.to_json(schedule)
        dateinterval.save()

        # TODO success
    except:
        # TODO some error
        pass


def add_financial_project(request):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    data = request.POST
    project_name = data.get('project_name')
    description = data.get('description')
    project_state = data.get('project_state')
    charity_id = data.get('charity_id')
    charity_user = get_object(User, id=charity_id)
    if charity_user is None:
        # TODO some error
        pass
    try:
        project = create_project(charity_user.charity, 'financial', project_name, description, project_state)
        target_money = data.get('target_money')
        current_money = data.get('current_money')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        financial_project = FinancialProject(project=project, target_money=target_money, current_money=current_money,
                                             start_date=start_date, end_date=end_date)
        financial_project.save()

        # TODO success
    except:
        # TODO some error
        pass


def edit_non_financial_project(request, pid):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure

    project = get_object(Project, id=pid)
    if project is None or project.nonfinancialproject is None:
        # TODO some error
        pass
    non_financial_project = project.nonfinancialproject
    if request.method == 'GET':
        # TODO url?
        return render(request, 'url', {
            'charity_id': project.charity.id,
            'project_name': project.project_name,
            'description': project.description,
            'project_state': project.project_state,
            'ability_type_id': non_financial_project.ability_type.id,
            'min_age': non_financial_project.min_age,
            'max_age': non_financial_project.max_age,
            'required_gender': non_financial_project.required_gender,
            'country': non_financial_project.country,
            'province': non_financial_project.province,
            'city': non_financial_project.city,
            'start_date': non_financial_project.dateinterval.begin_date,
            'end_date': non_financial_project.dateinterval.end_date,
            'schedule': non_financial_project.dateinterval.from_json()
        })
    elif request.method == 'POST':
        data = request.POST
        charity_id = data.get('charity_id')
        if charity_id is None:
            charity_id = project.charity.id
        ability_type_id = data.get('ability_type_id')
        if ability_type_id is None:
            ability_type_id = non_financial_project.ability_type.id
        charity_user = get_object(User, id=charity_id)
        ability_type = get_object(AbilityType, id=ability_type_id)
        if charity_user is None or ability_type is None:
            # TODO some error
            pass
        project_name = data.get('project_name')
        if not (project_name is None or len(project_name) == 0):
            project.project_name = project_name
        description = data.get('description')
        if not (description is None or len(description) == 0):
            project.description = description
        project_state = data.get('project_state')
        if not (project_state is None or len(project_state) == 0):
            project.project_state = project_state
        min_age = data.get('min_age')
        if not (min_age is None):
            non_financial_project.min_age = min_age
        max_age = data.get('max_age')
        if not (max_age is None):
            non_financial_project.max_age = max_age
        required_gender = data.get('required_gender')
        if not (required_gender is None or len(required_gender) == 0):
            non_financial_project.required_gender = required_gender
        country = data.get('country')
        if not (country is None or len(country) == 0):
            non_financial_project.country = country
        province = data.get('province')
        if not (province is None or len(province) == 0):
            non_financial_project.province = province
        city = data.get('city')
        if not (city is None or len(city) == 0):
            non_financial_project.city = city
        start_date = data.get('start_date')
        if not (start_date is None):
            non_financial_project.dateinterval.begin_date = start_date
        end_date = data.get('end_date')
        if not (end_date is None):
            non_financial_project.dateinterval.end_date = end_date
        schedule = data.get('schedule')
        if not (schedule is None or len(schedule) == 0):
            non_financial_project.dateinterval.to_json(schedule)
        non_financial_project.dateinterval.save()
        project.save()
        non_financial_project.save()
        # TODO url?
        return render(request, 'url', {})
    # TODO do something?


def edit_financial_project(request, pid):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure

    project = get_object(Project, id=pid)
    if project is None or project.financialproject is None:
        # TODO some error
        pass
    financial_project = project.financialproject
    if request.method == 'GET':
        # TODO url?
        return render(request, 'url', {
            'charity_id': project.charity.id,
            'project_name': project.project_name,
            'description': project.description,
            'project_state': project.project_state,
            'target_money': financial_project.target_money,
            'current_money': financial_project.current_money,
            'start_date': financial_project.start_date,
            'end_date': financial_project.end_date
        })
    elif request.method == 'POST':
        data = request.POST
        charity_id = data.get('charity_id')
        if charity_id is None:
            charity_id = project.charity.id
        charity_user = get_object(User, id=charity_id)
        if charity_user is None:
            # TODO some error
            pass
        project_name = data.get('project_name')
        if not (project_name is None or len(project_name) == 0):
            project.project_name = project_name
        description = data.get('description')
        if not (description is None or len(description) == 0):
            project.description = description
        project_state = data.get('project_state')
        if not (project_state is None or len(project_state) == 0):
            project.project_state = project_state
        target_money = data.get('target_money')
        if not (target_money is None or len(target_money) == 0):
            financial_project.target = target_money
        current_money = data.get('current_money')
        if not (current_money is None or len(current_money) == 0):
            financial_project.current_money = current_money
        start_date = data.get('start_date')
        if not (start_date is None or len(start_date) == 0):
            financial_project.start_date = start_date
        end_date = data.get('end_date')
        if not (end_date is None or len(end_date) == 0):
            financial_project.end_date = end_date
        project.save()
        financial_project.save()
        # TODO url?
        return render(request, 'url', {})
        # TODO do something?


def delete_non_financial_project(request, pid):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    project = get_object(Project, id=pid)
    if project is None:
        # TODO some error
        pass
    try:
        project.delete()
    except:
        # TODO something
        pass
    # TODO idk, do something?


def delete_financial_project(request, pid):
    secure = handle_admin_security(request)
    if type(secure) is HttpResponse:
        return secure
    project = get_object(Project, id=pid)
    if project is None:
        # TODO some error
        pass
    try:
        project.delete()
    except:
        # TODO something
        pass
    # TODO idk, do something?


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
    if type(secure) == HttpResponse:
        return secure
    try:
        charities = Charity.objects.all()
        charity_update_logs = {log for log in Log.objects.all() if
                               log.first_actor.is_charity and log.log_type == 'account_update'}
        # FIXME fix url
        context = {
            'all_charities': list(charities),
            'update_logs': list(charity_update_logs),
        }
        template = loader.get_template('accounts/admin-charity.html')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', 'Home')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_get_benefactors(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    try:
        benefactors = Benefactor.objects.all()
        benefactor_update_logs = {log for log in Log.objects.all() if
                                  log.first_actor.is_benefactor and log.log_type == 'account_update'}
        # FIXME fix url
        context = {
            'all_benefactors': list(benefactors),
            'update_logs': list(benefactor_update_logs),
        }
        template = loader.get_template('accounts/admin-user.html')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', 'Home')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_get_tags(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    try:
        tags = AbilityTag.objects.all()
        context = {'tags': tags}
        template = loader.get_template('accounts/admin-tag.html')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', 'admin')
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
    if type(secure) == HttpResponse:
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
        inactive_users = User.objects.filter(admin_approved=False, is_active=True).all()
        request_list = list(AbilityRequest.objects.all())
        admins = list(User.objects.filter(is_admin=True))
        context = {
            'charity_count': charity_count,
            'benefactor_count': benefactor_count,
            'project_count': project_count,
            'contributions_sum': contributions_sum,
            'tag_count': tag_count,
            'ability_type_count': ability_type_count,
            'score_count': score_count,
            'comment_count': comment_count,
            'inactive_users': inactive_users,
            'request_list': request_list,
            'admins': admins,
        }
        # TODO Fix template path and Redirect
        template = loader.get_template('accounts/admin.html')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page', 'Home')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def deactivate_user(request, uid):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    user = get_object(User, id=uid)
    try:
        user.admin_approved = False
        user.save()
        mail = EmailMessage('Account Rejected', 'حساب کاربری شما رد شد.', to=[user.email])
        mail.send()
        return HttpResponseRedirect(reverse('admin'))
    except:
        if user.is_benefactor:
            context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page',
                                             'admin_benefactor')
        else:
            context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page',
                                             'admin_charity')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def activate_user(request, uid):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    user = get_object(User, id=uid)
    try:
        user.admin_approved = True
        user.save()
        mail = EmailMessage('Account Approved', 'حساب کاربری شما تایید شد.', to=[user.email])
        mail.send()
        return HttpResponseRedirect(reverse('admin'))
    except:
        if user.is_benefactor:
            context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page',
                                             'admin_benefactor')
        else:
            context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page',
                                             'admin_charity')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_add_benefactor(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure

    test1_user = User.objects.filter(username=request.POST.get("username"))
    test2_user = User.objects.filter(username=request.POST.get("email"))
    if test1_user.__len__() != 0 and test2_user.__len__() != 0:
        context = error_context_generate('Invalid Data', 'Account already exists!', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))

    if test1_user.__len__() == 0 and len(test2_user) != 0:
        context = error_context_generate('Invalid Data', 'Email is Already Taken!', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))

    if len(test1_user) != 0 and len(test2_user) == 0:
        context = error_context_generate('Invalid Data', 'Username is Already Taken!', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))

    tmp_contact_info = ContactInfo.objects.create(country="ایران",
                                                  province=request.POST.get("province"),
                                                  city=request.POST.get("city"),
                                                  address=request.POST.get("address"),
                                                  postal_code=request.POST.get("postal_code"),
                                                  phone_number=request.POST.get("phone_number")
                                                  )
    tmp_user = User.objects.create(username=request.POST.get("username"), password=request.POST.get("password"),
                                   email=request.POST.get("email"), contact_info=tmp_contact_info,
                                   description=request.POST.get("description"))
    tmp_user.is_active = True
    tmp_user.admin_approved = True
    tmp_user.save()
    Logger.create_account(tmp_user, None, None)
    # if request.POST.get("account_type") == "Charity":
    #     tmp_user.is_charity = True
    #     tmp_charity = Charity.objects.create(user=tmp_user, name=request.POST.get("charity_name"))
    #     tmp_charity.save()
    #     tmp_user.save()
    #
    #     login(request, tmp_user)
    #     Logger.login(request.user, None, None)
    #     return HttpResponseRedirect(reverse('accounts:user_profile'))
    #
    #
    # else:
    tmp_user.is_benefactor = True
    tmp_benefactor = Benefactor.objects.create(user=tmp_user, first_name=request.POST.get("first_name"),
                                               last_name=request.POST.get("last_name"),
                                               age=request.POST.get("age"), gender=request.POST.get('gender'))
    tmp_benefactor.save()
    tmp_user.save()
    # login(request, tmp_user)
    # Logger.login(request.user, None, None)
    return HttpResponseRedirect(reverse('admin_benefactor'))


def admin_edit_benefactor_data(request, uid):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    user = get_object(User, id=uid)
    try:
        notifications = Notification.objects.filter(user=user).all()
        context = {"type": user.is_charity, "username": user.username, "email": user.email,
                   "country": user.contact_info.country, "province": user.contact_info.province,
                   "city": user.contact_info.city, "address": user.contact_info.address,
                   "phone_number": user.contact_info.phone_number, "description": user.description,
                   "notifications": notifications}
        if user.is_benefactor:
            try:
                benefactor = get_object(Benefactor, user=user)
                projects = {project for project in Project.objects.all() if benefactor in project.benefactors}
                context['project_count'] = len(projects)
                # abilities = benefactor.ability_set.all()
                score = benefactor.calculate_score()
                context['score'] = score
                context["first_name"] = benefactor.first_name
                context["last_name"] = benefactor.last_name
                context["gender"] = benefactor.gender
                context["age"] = benefactor.age
                context["credit"] = benefactor.credit
            except:
                context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page',
                                                 'admin_benefactor')
                template = loader.get_template('accounts/error_page.html')
                return HttpResponse(template.render(context, request))

        else:
            context = error_context_generate('Account Type Error', 'Selected Account is not a Benefactor',
                                             'admin_benefactor')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))

        return HttpResponseRedirect('admin_benefactor')
    except:
        context = error_context_generate('Unexpected Error', 'Error Getting Account Data!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_edit_benefactor(request, uid):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    user = get_object(User, id=uid)
    try:
        if user.is_charity:
            context = error_context_generate('Account Type Error', 'Selected Account is not a Benefactor',
                                             'admin_benefactor')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        if request.POST.get('password') is not None:
            user.password = request.POST.get("password")
        if request.POST.get('description') is not None:
            user.description = request.POST.get("description")
        if request.POST.get("province") is not None:
            user.contact_info.province = request.POST.get("province")
        if request.POST.get("city") is not None:
            user.contact_info.city = request.POST.get("city")
        if request.POST.get("address") is not None:
            user.contact_info.address = request.POST.get("address")
        if request.POST.get("phone_number") is not None:
            user.contact_info.phone_number = request.POST.get("phone_number")
        user.save()
        user.contact_info.save()
        if request.POST.get("first_name") is not None and len(request.POST.get("first_name")) > 0:
            user.benefactor.first_name = request.POST.get("first_name")
        if request.POST.get("last_name") is not None and len(request.POST.get("last_name")) > 0:
            user.benefactor.last_name = request.POST.get("last_name")
        if request.POST.get("gender") is not None:
            user.benefactor.gender = request.POST.get("gender")
        if request.POST.get("age") is not None:
            user.benefactor.age = request.POST.get("age")
        user.benefactor.save()
        Logger.account_update(user, None, None)
        # TODO Fix Redirect
        return HttpResponseRedirect(reverse('accounts:user_profile'))
    except:
        context = error_context_generate('Unexpected Error', 'Error Getting Account Data!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_add_charity(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure

    test1_user = User.objects.filter(username=request.POST.get("username"))
    test2_user = User.objects.filter(username=request.POST.get("email"))
    if test1_user.__len__() != 0 and test2_user.__len__() != 0:
        context = error_context_generate('Invalid Data', 'Account already exists!', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))

    if test1_user.__len__() == 0 and len(test2_user) != 0:
        context = error_context_generate('Invalid Data', 'Email is Already Taken!', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))

    if len(test1_user) != 0 and len(test2_user) == 0:
        context = error_context_generate('Invalid Data', 'Username is Already Taken!', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))

    tmp_contact_info = ContactInfo.objects.create(country="ایران",
                                                  province=request.POST.get("province"),
                                                  city=request.POST.get("city"),
                                                  address=request.POST.get("address"),
                                                  postal_code=request.POST.get("postal_code"),
                                                  phone_number=request.POST.get("phone_number")
                                                  )
    tmp_user = User.objects.create(username=request.POST.get("username"), password=request.POST.get("password"),
                                   email=request.POST.get("email"), contact_info=tmp_contact_info,
                                   description=request.POST.get("description"))
    tmp_user.is_active = True
    tmp_user.admin_approved = True
    tmp_user.save()
    Logger.create_account(tmp_user, None, None)
    # if request.POST.get("account_type") == "Charity":
    tmp_user.is_charity = True
    tmp_charity = Charity.objects.create(user=tmp_user, name=request.POST.get("charity_name"))
    tmp_charity.save()
    tmp_user.save()

    # login(request, tmp_user)
    # Logger.login(request.user, None, None)
    return HttpResponseRedirect(reverse('admin_benefactor'))
    #
    #
    # # else:
    # tmp_user.is_benefactor = True
    # tmp_benefactor = Benefactor.objects.create(user=tmp_user, first_name=request.POST.get("first_name"),
    #                                            last_name=request.POST.get("last_name"),
    #                                            age=request.POST.get("age"), gender=request.POST.get('gender'))
    # tmp_benefactor.save()
    # tmp_user.save()
    # # login(request, tmp_user)
    # # Logger.login(request.user, None, None)
    # return HttpResponseRedirect(reverse('admin_benefactor'))


def admin_edit_charity_data(request, uid):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    user = get_object(User, id=uid)
    try:
        notifications = Notification.objects.filter(user=user).all()
        context = {"type": user.is_charity, "username": user.username, "email": user.email,
                   "country": user.contact_info.country, "province": user.contact_info.province,
                   "city": user.contact_info.city, "address": user.contact_info.address,
                   "phone_number": user.contact_info.phone_number, "description": user.description,
                   "notifications": notifications}
        if user.is_charity:
            try:
                charity = get_object(Benefactor, user=user)
                context["name"] = charity.name
                context["score"] = charity.calculate_score()
            except:
                context = error_context_generate('Unexpected Error', 'There Was a Problem in Loading the Page',
                                                 'admin_benefactor')
                template = loader.get_template('accounts/error_page.html')
                return HttpResponse(template.render(context, request))

        else:
            context = error_context_generate('Account Type Error', 'Selected Account is not a Charity',
                                             'admin_benefactor')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))

        return HttpResponseRedirect('admin_benefactor')
    except:
        context = error_context_generate('Unexpected Error', 'Error Getting Account Data!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_edit_charity(request, uid):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    user = get_object(User, id=uid)
    try:
        if user.is_benefactor:
            context = error_context_generate('Account Type Error', 'Selected Account is not a Charity',
                                             'admin_benefactor')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        if request.POST.get('password') is not None:
            user.password = request.POST.get("password")
        if request.POST.get('description') is not None:
            user.description = request.POST.get("description")
        if request.POST.get("province") is not None:
            user.contact_info.province = request.POST.get("province")
        if request.POST.get("city") is not None:
            user.contact_info.city = request.POST.get("city")
        if request.POST.get("address") is not None:
            user.contact_info.address = request.POST.get("address")
        if request.POST.get("phone_number") is not None:
            user.contact_info.phone_number = request.POST.get("phone_number")
        user.save()
        user.contact_info.save()
        if request.POST.get("name") is not None and len(request.POST.get("name")) > 0:
            user.charity.name = request.POST.get("name")
        user.charity.save()
        Logger.account_update(user, None, None)
        # TODO Fix Redirect
        return HttpResponseRedirect(reverse('admin'))
    except:
        context = error_context_generate('Unexpected Error', 'Error Getting Account Data!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_delete_user(request, uid):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    user = get_object(User, id=uid)
    # TODO Email To User
    try:
        if user != request.user:
            user.delete()
        # TODO Fix Redirect Path
        return HttpResponseRedirect(reverse('admin'))
    except:
        context = error_context_generate('Unexpected Error', 'Apparently This Little Dude is Invulnerable!',
                                         'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_get_contributions(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    try:
        context = {
            'contributions': FinancialContribution.objects.all()
        }
        # TODO Fix Template Path
        template = loader.get_template('accounts/admin-tx.html')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'Error Getting Page Data!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_get_scores(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    try:
        score_list = list(BenefactorScore.objects.all())
        score_list.extend(list(CharityScore.objects.all()))
        score_logs = list(Log.objects.filter(log_type='submit_score').all())
        context = {
            'scores': score_list,
            'score_logs':score_logs
        }
        # TODO Fix Path
        template = loader.get_template('accounts/admin-score.html')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'Error Getting Page Data!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_get_comments(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    try:
        comment_list = list(BenefactorComment.objects.all())
        comment_list.extend(list(CharityComment.objects.all()))
        comment_logs = list(Log.objects.filter(log_type='submit_comment').all())
        context = {
            'comments': comment_list,
            'comment_logs': comment_logs,
        }
        # TODO Fix Path
        template = loader.get_template('accounts/admin-comment.html')
        return HttpResponse(template.render(context, request))
    except:
        context = error_context_generate('Unexpected Error', 'Error Getting Page Data!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_add_benefactor_comment(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    try:
        benefactor = get_object(User, id=request.POST.get('benefactor')).benefactor
        charity = get_object(Charity, id=request.POST.get('charity')).charity
        ability_type = get_object(Ability, id=request.POST.get('ability_type'))
        ability = benefactor.ability_set.filter(ability_type=ability_type).all()[0]
        if ability is None:
            context = error_context_generate('Not Found', 'Requested Benefactor Does Not Have such Ability', 'admin')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        comment = get_object(BenefactorComment, commenter=charity, commented=benefactor, ability=ability)
        if comment is None:
            comment = BenefactorComment.objects.create(commenter=charity, commented=benefactor, ability=ability)
        comment.comment_string = request.POST.get('comment_string')
        comment.save()
        return HttpResponseRedirect(reverse('admin_comment'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Submitting Comment!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_edit_benefactor_comment(request, comment_id):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    comment = get_object(BenefactorComment, id=comment_id)
    if comment is None:
        # TODO Error Comment
        context = error_context_generate('Not Found', 'Requested Comment Cannot be Found', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        comment.comment_string = request.POST.get('comment_string')
        comment.save()
        return HttpResponseRedirect(reverse('admin_comment'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Editing Comment!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_delete_benefactor_comment(request, comment_id):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    comment = get_object(BenefactorComment, id=comment_id)
    if comment is None:
        # TODO Error Comment
        context = error_context_generate('Not Found', 'Requested Comment Cannot be Found', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        comment.delete()
        return HttpResponseRedirect(reverse('admin_comment'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Deleting Comment!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_add_charity_comment(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    try:
        charity = get_object(User, id=request.POST.get('charity')).charity
        benefactor = get_object(User, id=request.POST.get('benefactor')).benefactor
        comment = get_object(CharityComment, commenter=benefactor, commented=charity)
        if comment is None:
            comment = CharityComment.objects.create(commenter=benefactor, commented=charity)
        comment.comment_string = request.POST.get('comment_string')
        comment.save()
        return HttpResponseRedirect(reverse('admin_comment'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Submitting Comment!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_edit_charity_comment(request, comment_id):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    comment = get_object(CharityComment, id=comment_id)
    if comment is None:
        # TODO Error Comment
        context = error_context_generate('Not Found', 'Requested Comment Cannot be Found', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        comment.comment_string = request.POST.get('comment_string')
        comment.save()
        return HttpResponseRedirect(reverse('admin_comment'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Editing Comment!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_delete_charity_comment(request, comment_id):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    comment = get_object(CharityComment, id=comment_id)
    if comment is None:
        # TODO Error Comment
        context = error_context_generate('Not Found', 'Requested Comment Cannot be Found', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        comment.delete()
        return HttpResponseRedirect(reverse('admin_comment'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Deleting Comment!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_add_benefactor_score(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    try:
        benefactor = get_object(User, id=request.POST.get('benefactor')).benefactor
        ability_type = get_object(AbilityType, id=request.POST.get('ability_type'))
        charity = get_object(User, id=request.POST.get('charity')).charity
        ability = benefactor.ability_set.filter(ability_type=ability_type).all()[0]
        score = get_object(BenefactorScore, charity=charity, benefactor=benefactor, ability=ability)
        if score is None:
            score = BenefactorScore.objects.create(charity=charity, benefactor=benefactor, ability=ability)
        if float(request.POST.get('score')) > 10.0:
            score.score = 10.0
        else:
            score.score = float(request.POST.get('score'))
        score.save()
        return HttpResponseRedirect(reverse('admin_score'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Submitting Score!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_edit_benefactor_score(request, score_id):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    score = get_object(BenefactorScore, id=score_id)
    if score is None:
        # TODO Error score
        context = error_context_generate('Not Found', 'Requested score Cannot be Found', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        if float(request.POST.get('score')) > 10.0:
            score.score = 10.0
        else:
            score.score = float(request.POST.get('score'))
        score.save()
        return HttpResponseRedirect(reverse('admin_score'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Editing score!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_delete_benefactor_score(request, score_id):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    score = get_object(BenefactorScore, id=score_id)
    if score is None:
        # TODO Error score
        context = error_context_generate('Not Found', 'Requested Score Cannot be Found', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        score.delete()
        return HttpResponseRedirect(reverse('admin_score'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Deleting score!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_add_charity_score(request):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    try:
        charity = get_object(User, id=request.POST.get('charity')).charity
        benefactor = get_object(User, id=request.POST.get('benefactor')).benefactor
        score = get_object(CharityScore, benefactor=benefactor, charity=charity)
        if score is None:
            score = CharityScore.objects.create(benefactor=benefactor, charity=charity)
        if float(request.POST.get('score')) > 10.0:
            score.score = 10.0
        else:
            score.score = float(request.POST.get('score'))
        score.save()
        return HttpResponseRedirect(reverse('admin_score'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Submitting Score!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_edit_charity_score(request, score_id):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    score = get_object(CharityScore, id=score_id)
    if score is None:
        # TODO Error Comment
        context = error_context_generate('Not Found', 'Requested Comment Cannot be Found', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        if float(request.POST.get('score')) > 10.0:
            score.score = 10.0
        else:
            score.score = float(request.POST.get('score'))
        score.save()
        return HttpResponseRedirect(reverse('admin_score'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Editing Comment!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def admin_delete_charity_score(request, score_id):
    secure = handle_admin_security(request)
    if type(secure) == HttpResponse:
        return secure
    score = get_object(CharityScore, id=score_id)
    if score is None:
        # TODO Error Comment
        context = error_context_generate('Not Found', 'Requested Comment Cannot be Found', 'admin')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        score.delete()
        return HttpResponseRedirect(reverse('admin_score'))
    except:
        context = error_context_generate('Unexpected Error', 'Error in Deleting Comment!', 'admin')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
