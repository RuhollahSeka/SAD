from django.core.mail import EmailMessage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from projects.models import FinancialProject, NonFinancialProject, Project, Log, Ability, FinancialContribution
####### Danial imports .Some of them may be redundant!!!

from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from accounts.forms import CharitySignUpForm
from accounts.models import *
from projects.models import CooperationRequest, search_charity, search_benefactor
from accounts.log_util import Logger
import random, string

possible_characters = string.ascii_letters + string.digits
ip = '127.0.0.1:8000/'


def generate_recover_string(length=32):
    rng = random.SystemRandom()
    return "".join([rng.choice(possible_characters) for i in range(length)])


def get_object(obj_class, *args, **kwargs):
    try:
        obj_set = obj_class.objects.filter(*args, **kwargs)
        if obj_set.count() <= 0:
            return None
        return obj_set.all()[0]
    except:
        # TODO Raise Super Ultra Error
        return 'Error'


def error_context_generate(error_title, error_message, redirect_address):
    return {
        'error_title': error_title,
        'error_message': error_message,
        'redirect_address': redirect_address
    }


# Create your views here.

def all_user_projects(request):
    if not request.user.is_charity:
        pass
    projects = request.user.charity.project_set
    return render(request, 'url', {
        'all_user_projects': projects
    })


def add_ability_to_benefactor(request):
    benefactor_id = request.POST.get('add_ability_benefactor_id')
    if request.user.id != benefactor_id:
        # TODO Return Error
        context = error_context_generate('Authentication Error', 'You Don\'t Have Permission to Change this Account!',
                                         '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))

    ability_type_name = request.POST.get('add_ability_ability_type_name')
    ability_description = request.POST.get('add_ability_description')
    ability_type = AbilityType.objects.all().filter(name__iexact=ability_type_name)[0]
    benefactor = Benefactor.objects.all().filter(user_id=benefactor_id)[0]
    ability = Ability(benefactor=benefactor, ability_type=ability_type, description=ability_description)
    ability.save()
    benefactor.ability_set.add(ability)
    Logger.add_ability_benefactor(request.user, None, None)
    # TODO Fix Path
    return HttpResponseRedirect('path')

def submit_benefactor_score(request, benefactor_username):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = error_context_generate('Authentication Error', 'You are not Signed In!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_benefactor:
        # TODO Raise Account Type Error
        context = error_context_generate('Account Type Error', 'You Can\'t Submit Score for Another Benefactor!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        charity = get_object(Charity, user=request.user)
        benefactor = get_object(Benefactor, user=get_object(User, username=benefactor_username))
        if charity.benefactor_history.filter(user=benefactor.user).count() <= 0:
            context = error_context_generate('No Cooperation Error',
                                             'You Cannot Submit Score for a Benefactor with Whom You Had no Cooperation!',
                                             '')
            # TODO Raise No_Cooperation Error
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        ability = get_object(AbilityType, benefactor=benefactor, name=request.POST.get('ability_type'))
        score = charity.benefactorscore_set.get(benefactor=benefactor, charity=charity)
        if score is None:
            score = BenefactorScore.objects.create(ability_type=ability, benefactor=benefactor,
                                                   charity=get_object(Charity, user=request.user))
        score.score = int(request.POST.get('score'))
        score.save()
        Logger.submit_score(request.user, benefactor.user, None)
        return HttpResponseRedirect([])
    except:
        context = error_context_generate('Unexpected Error', 'Some of the Data Needed for The Page is Lost or Damaged',
                                         '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
        # TODO raise error


def submit_charity_score(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = error_context_generate('Authentication Error', ' You are not Signed In!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_charity:
        context = error_context_generate('Account Type Error', 'You Can\'t Submit Score for Another Charity!', '')
        # TODO Raise Account Type Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    benefactor = get_object(Benefactor, user=request.user)
    if benefactor.charity_set.get(user=get_object(User, username=request.POST.get('charity_username'))).count <= 0:
        context = error_context_generate('No Cooperation Error',
                                         'You Cannot Submit Score for a Charity with Which You Had no Cooperation!', '')
        # TODO Raise No_Cooperation Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        charity = get_object(Charity, user=get_object(User, username=request.POST.get('charity_username')))
        score = benefactor.charityscore_set.get(benefactor=benefactor, charity=charity)
        if score is None:
            score = get_object(CharityScore, charity=charity, benefactor=get_object(Benefactor, user=request.user))
        score.score = int(request.POST.get('score'))
        score.save()
        Logger.submit_score(request.user, charity.user, None)
        return HttpResponseRedirect([])
    except:
        # TODO raise error
        context = error_context_generate('Unexpected Error', 'Some of the Data Needed for The Page is Lost or Damaged',
                                         '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def submit_ability_request(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = error_context_generate('Authentication Error', 'You are not Signed In!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        new_request = AbilityRequest.objects.create(type=request.POST.get('type'), name=request.POST.get('name'),
                                                    description=request.POST.get('description'))
        new_request.save()

        Logger.request_new_ability_type(request.user, None, None)
        return HttpResponseRedirect([])
    except:
        # TODO Raise Error
        context = error_context_generate('Unexpected Error', 'Some of the Data Needed for The Page is Lost or Damaged',
                                         '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def submit_cooperation_request(request, project_id):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = error_context_generate('Authentication Error', 'You are not Signed In!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        # FIXME How should we find the project? I mean which data is given to find the project with?
        project = NonFinancialProject.objects.all().filter(project_id=project_id)
        if request.user.is_benefactor:
            benefactor = get_object(Benefactor, user=request.user)
            charity = get_object(Charity, user=get_object(User, username=request.POST.get('username')))
            new_notification = Notification.objects.create(type='new_request', user=charity.user,
                                                           datetime=datetime.datetime.now())
            new_notification.description = 'A new Cooperation Request is Received for Project ' + project.project
            new_notification.save()
            Logger.request_submit(request.user, charity.user, project.project)
            request_type = 'b2c'
        else:
            benefactor = get_object(Benefactor, user=get_object(User, username=request.POST.get('username')))
            charity = get_object(Charity, user=request.user)
            new_notification = Notification.objects.create(type='new_request', user=benefactor.user,
                                                           datetime=datetime.datetime.now())
            new_notification.description = 'A new Cooperation Request Has Been Received!'
            new_notification.save()
            Logger.request_submit(request.user, benefactor.user, project.project)
            request_type = 'c2b'
        new_request = CooperationRequest.objects.create(benefactor=benefactor, charity=charity, type=request_type,
                                                        description=request.POST.get('description'))
        new_request.nonfinancialproject = project
        new_request.save()
        return HttpResponseRedirect([])
    except:
        # TODO Raise Error
        context = {
            'error_message': 'Unexpected Error: Some of the Data Needed for The Page is Lost or Damaged'
        }
        context = error_context_generate('Unexpected Error', 'Some of the Data Needed for The Page is Lost or Damaged',
                                         '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


#################################################################
#################################################################
#################################################################
# ignore this block


class CharitySignUpView(CreateView):
    model = User
    form_class = CharitySignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        print('Azed')
        kwargs['user_type'] = 'charity'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('charity_signup')


#################################################################
#################################################################
#################################################################


#####Signup

class SignUpView(TemplateView):
    template_name = "accounts/register.html"


@csrf_exempt
def signup(request):
    # try:

    test1_user = User.objects.filter(username=request.POST.get("username"))
    test2_user = User.objects.filter(username=request.POST.get("email"))
    if test1_user.__len__() != 0 and test2_user.__len__() != 0:
        return render(request, 'accounts/register.html',
                      {'error_message': 'Account already exists! Try login or forget password.'})

    if test1_user.__len__() == 0 and len(test2_user) != 0:
        return render(request, 'accounts/register.html', {'error_message': 'Email is already taken!  '})

    if len(test1_user) != 0 and len(test2_user) == 0:
        return render(request, 'accounts/register.html',
                      {'error_message': 'Username is already taken! try another username.  '})

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
    tmp_user.is_active = False
    tmp_user.save()
    code = generate_recover_string()
    message = 'برای فعال شدن حساب خود بر روی لینک زیر کلیک کنید:' + '\n'
    message += 'url/' + str(tmp_user.id) + '/' + code
    tmp_user.activation_string = code
    email_message = EmailMessage('Activation Email', 'برای فعال شدن حساب خود بر روی لینک زیر کلیک کنید:' + '\n',
                                 to=tmp_user.email)
    email_message.send()
    Logger.create_account(tmp_user, None, None)
    if request.POST.get("account_type") == "Charity":
        tmp_user.is_charity = True
        tmp_charity = Charity.objects.create(user=tmp_user, name=request.POST.get("charity_name"))
        tmp_charity.save()
        tmp_user.save()

        login(request, tmp_user)
        Logger.login(request.user, None, None)
        return HttpResponseRedirect(reverse('accounts:user_profile'))


    else:
        tmp_user.is_benefactor = True
        tmp_benefactor = Benefactor.objects.create(user=tmp_user, first_name=request.POST.get("first_name"),
                                                   last_name=request.POST.get("last_name"),
                                                   age=request.POST.get("age"), gender=request.POST.get('gender'))
        tmp_benefactor.save()
        tmp_user.save()
        login(request, tmp_user)
        Logger.login(request.user, None, None)
        return HttpResponseRedirect(reverse('accounts:benefactor_dashboard'))


# except:
#     context = error_context_generate('Signup Error!', 'Error While Creating New Account!', 'accounts:signup_view')
#     template = loader.get_template('accounts/error_page.html')
#     return HttpResponse(template.render(context, request))


def activate_user(request, uid, activation_string):
    # TODO any security stuff?
    users = User.objects.filter(id=uid)
    if users.count() != 1:
        # TODO shitty link
        context = error_context_generate('Activation Error', 'Something Went Wrong in Activating Your Account!', 'Home')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    user = users[0]
    if user.activation_string != activation_string:
        # TODO shitty link
        context = error_context_generate('Invalid Key Error', 'Your Provided Activation Key is not Valid', 'Home')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    user.is_active = True
    # TODO activation success
    return HttpResponseRedirect(reverse('Home'))


####Login

class LoginView(TemplateView):
    template_name = "accounts/login.html"


def benefactor_dashboard(request):
    user = request.user
    if not user.is_authenticated or not user.is_benefactor:
        # TODO error
        pass
    requests = CooperationRequest.objects.filter(type__iexact='c2b').filter(benefactor=user.benefactor).filter(
            state__iexact='on-hold')
    notifications = Notification.objects.filter(user=user)
    user_project_ids = [project.id for project in user.benefactor.project_set.all()]
    complete_project_count = Project.objects.filter(project_state__iexact='completed').filter(id__in=user_project_ids).count()
    non_complete_project_count = Project.objects.filter(project_state__iexact='in-progress').filter(id__in=
                                                                                                    user_project_ids).count()
    if request.method == 'GET':
        return render(request, 'accounts/user-dashboard.html', {
            'requests': list(requests),
            'a_notification': notifications[0] if notifications.count() != 0 else None,
            'have_notification': True if notifications.count() > 0 else False,
            'notifications': list(notifications),
            'charity_results': [],
            'complete_project_count': complete_project_count,
            'non_complete_project_count': non_complete_project_count
        })
    elif request.method == 'POST':
        post = request.POST

        name = post.get('name')
        min_score = post.get('min_score')
        max_score = post.get('max_score')
        min_related_projects = post.get('min_related_projects')
        max_related_projects = post.get('max_related_projects')
        min_finished_projects = post.get('min_finished_projects')
        max_finished_projects = post.get('max_finished_projects')
        benefactor_name = post.get('benefactor_name')
        country = post.get('country')
        province = post.get('province')
        city = post.get('city')
        charity_result = search_charity(name=name, min_score=min_score, max_score=max_score,
                                        min_related_projects=min_related_projects,
                                        max_related_projects=max_related_projects,
                                        min_finished_projects=min_finished_projects,
                                        max_finished_projects=max_finished_projects, benefactor_name=benefactor_name,
                                        country=country, province=province, city=city)

        return render(request, 'accounts/user-dashboard.html', {
            'requests': list(requests),
            'a_notification': notifications[0] if notifications.count() != 0 else None,
            'have_notification': True if notifications.count() > 0 else False,
            'notifications': list(notifications),
            'charity_results': list(charity_result),
            'complete_project_count': complete_project_count,
            'non_complete_project_count': non_complete_project_count
        })


def charity_dashboard(request):
    user = request.user
    if not user.is_authenticated or not user.is_charity:
        # TODO error
        pass
    requests = CooperationRequest.objects.filter(type__iexact='b2c').filter(benefactor=user.benefactor).filter(
            state__iexact='on-hold')
    notifications = Notification.objects.filter(user=user)
    user_project_ids = [project.id for project in user.charity.project_set]
    complete_project_count = Project.objects.filter(project_state__iexact='completed').filter(id__in=user_project_ids).count()
    non_complete_project_count = Project.objects.filter(project_state__iexact='in-progress').filter(id__in=
                                                                                                    user_project_ids).count()
    if request.method == 'GET':
        return render(request, 'url', {
            'requests': list(requests),
            'a_notification': notifications[0] if notifications.count() != 0 else None,
            'have_notification': True if notifications.count() > 0 else False,
            'notifications': list(notifications),
            'benefactor_results': [],
            'complete_project_count': complete_project_count,
            'non_complete_project_count': non_complete_project_count
        })
    elif request.method == 'POST':
        post = request.POST
        start_date = post.get('start_date')
        end_date = post.get('end_date')
        weekly_schedule = json.loads(post.get('schedule'))
        schedule = [start_date, end_date, weekly_schedule]
        min_required_hours = post.get('min_required_hours')
        min_date_overlap = post.get('min_date_overlap')
        min_time_overlap = post.get('min_time_overlap')
        tags = post.get('tags')
        ability_name = post.get('ability_name')
        ability_min_score = post.get('ability_min_score')
        ability_max_score = post.get('ability_max_score')
        country = post.get('country')
        province = post.get('province')
        city = post.get('city')
        user_min_score = post.get('user_min_score')
        user_max_score = post.get('user_max_score')
        gender = post.get('gender')
        first_name = post.get('first_name')
        last_name = post.get('last_name')
        result_benefactor = search_benefactor(schedule, min_required_hours, min_date_overlap, min_time_overlap,
                                              tags, ability_name, ability_min_score, ability_max_score, country,
                                              province, city, user_min_score, user_max_score, gender, first_name,
                                              last_name)
        return render(request, 'url', {
            'requests': list(requests),
            'a_notification': notifications[0] if notifications.count() != 0 else None,
            'have_notification': True if notifications.count() > 0 else False,
            'notifications': list(notifications),
            'benefactor_results': list(result_benefactor),
            'complete_project_count': complete_project_count,
            'non_complete_project_count': non_complete_project_count
        })


def dashboard(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'accounts/login.html', {'error_message': 'لطفاً اول وارد شوید'})
    if user.is_benefactor:
        HttpResponseRedirect(reverse('accounts:benefactor_dashboard'))
    if user.is_charity:
        HttpResponseRedirect(reverse('accounts:charity_dashboard'))
    else:
        pass


@csrf_exempt
def login_user(request):
    # tmp_user = get_object_or_404(User,username=request.POST.get("username"),password=request.POST.get("password"))
    # try:
    if request.user.is_authenticated:
        Logger.logout(request.user, None, None)
        logout(request)
    tmp_user = User.objects.filter(username=request.POST.get("username"))
    if len(tmp_user) == 0:
        return render(request, 'accounts/login.html', {'error_message': 'کاربر موردنظر یافت نشد!'})
    tmp_user = get_object(User, username=request.POST.get("username"))
    if tmp_user.password != request.POST.get("password"):
        return render(request, 'accounts/login.html', {'error_message': 'رمز اشتباهه -.-'})

    if tmp_user.is_charity:
        login(request, user=tmp_user)
        Logger.login(request.user, None, None)
        return render(request, 'accounts/charity.html')

    else:

        login(request, tmp_user)
        Logger.login(request.user, None, None)
        return HttpResponseRedirect(reverse('accounts:benefactor_dashboard'))


# except:
#     # TODO Redirect to Login
#     context = error_context_generate('Login Error', 'رمز یا ایمیل درست وارد نشده است', 'login_view')
#     template = loader.get_template('accounts/login.html')
#
#     return HttpResponseRedirect(reverse('accounts:user_profile'))


def recover_password(request):
    if request.method == 'GET':
        return render(request, 'accounts/recover_password.html')
    elif request.method == 'POST':
        email = request.POST.get("recover_email")
        user_queryset = User.objects.all().filter(email__iexact=email)
        if user_queryset.count() == 0:
            # TODO error no such user
            pass
        elif user_queryset.count() > 1:
            # TODO something went wrong
            pass
        user = user_queryset[0]
        current_recover_string = user.email_recover_string
        user_id = user.id
        recovery_url = ip + 'accounts/' + user_id + '/' + current_recover_string
        message = 'برای وارد کردن رمز جدید خود، وارد لینک زیر شوید:' + '\n'
        message += recovery_url
        recovery_email = EmailMessage('Password recovery', message, email)
        recovery_email.send()
        # TODO return something?


def recover_pwd(request, uid, rec_str):
    if request.method == 'GET':
        # todo what to do here?
        return render(request, 'accounts/enter_new_password.html')
    if request.method == 'POST':
        password = request.POST.get('recovery_password')
        user_queryset = User.objects.all().filter(id=uid)
        if user_queryset.count() != 1:
            # TODO shitty link
            pass
        user = user_queryset[0]
        recovery_string = user.email_recover_string
        if recovery_string != rec_str:
            # TODO shitty link
            pass
        user.email_recover_string = generate_recover_string()
        user.password = password
        # TODO successful password change


def user_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html', {'error_message': 'please login first'})
    print(request.user.is_charity)
    print(request.user.is_benefactor)
    # try:
    print(request.user)
    context = {"type": request.user.is_charity, "username": request.user.username, "email": request.user.email,
               "country": request.user.contact_info.country, "province": request.user.contact_info.province,
               "city": request.user.contact_info.city, "address": request.user.contact_info.address,
               "phone_number": request.user.contact_info.phone_number, 'description': request.user.description}
    if request.user.is_benefactor:
        # try:
        benefactor = get_object(Benefactor, user=request.user)
        context['user'] = benefactor
        context['benefactor'] = benefactor
        projects = {project for project in Project.objects.all() if benefactor in project.benefactors}
        context['project_count'] = len(projects)
        abilities = benefactor.ability_set.all()
        score = benefactor.calculate_score()
        print(request)
        context['score'] = score
        context["first_name"] = benefactor.first_name
        context["last_name"] = benefactor.last_name
        context["gender"] = benefactor.gender
        context["age"] = benefactor.age
        context["credit"] = benefactor.credit
        print(context)
        # print(context.__str__())
        # except:
        #     print(1)

    else:
        try:
            charity = get_object(Charity, user=request.user)
            context["name"] = charity.name
            context["score"] = charity.score
        except:
            print(1)
    return render(request, 'accounts/user-profile.html', context)
    # except:
    #     context = error_context_generate('Unexpected Error', 'Error Getting Account Data!', '')
    #     # TODO Raise Error
    #     template = loader.get_template('accounts/error_page.html')
    #     return HttpResponse(template.render(context, request))


#### Customize User

@csrf_exempt
def customize_user_data(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html', {'error_message': 'لطفاً اول وارد شوید'})

    if request.method == 'GET':
        return HttpResponseRedirect('accounts/user-profile.html')
    try:
        notifications = Notification.objects.filter(user=request.user).all()
        context = {"type": request.user.is_charity, "username": request.user.username, "email": request.user.email,
                   "country": request.user.contact_info.country, "province": request.user.contact_info.province,
                   "city": request.user.contact_info.city, "address": request.user.contact_info.address,
                   "phone_number": request.user.contact_info.phone_number, "description": request.user.description,
                   "notifications": notifications}
        if request.user.is_benefactor:
            try:
                benefactor = get_object(Benefactor, user=request.user)
                projects = {project for project in Project.objects.all() if benefactor in project.benefactors}
                context['project_count'] = len(projects)
                abilities = benefactor.ability_set.all()
                if benefactor.score <= 0:
                    score = 'N/A'
                else:
                    score = 0
                    for ability in abilities:
                        score += ability.score
                    score /= len(abilities)
                context['score'] = score
                context["first_name"] = benefactor.first_name
                context["last_name"] = benefactor.last_name
                context["gender"] = benefactor.gender
                context["age"] = benefactor.age
                context["credit"] = benefactor.credit
            except:
                print(1)


        else:
            try:
                context["name"] = request.user.charity.name
                context["score"] = request.user.charity.score
            except:
                print(1)

        return render(request, 'accounts/user-profile.html', context)
    except:
        context = error_context_generate('Unexpected Error', 'Error Getting Account Data!', '')
        # TODO Raise Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def customize_user(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = error_context_generate('Authentication Error', 'لطفاً اول وارد شوید', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not request.user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.POST.get('password') is not None:
        request.user.password = request.POST.get("password")
    if request.POST.get('description') is not None:
        request.user.description = request.POST.get("description")
    if request.POST.get("province") is not None:
        request.user.contact_info.province = request.POST.get("province")
    if request.POST.get("city") is not None:
        request.user.contact_info.city = request.POST.get("city")
    if request.POST.get("address") is not None:
        request.user.contact_info.address = request.POST.get("address")
    if request.POST.get("phone_number") is not None:
        request.user.contact_info.phone_number = request.POST.get("phone_number")
    request.user.save()
    if request.user.is_charity:
        if request.POST.get("name") is not None:
            request.user.charity.name = request.POST.get("name")
        request.user.charity.save()
    else:
        if request.POST.get("first_name") is not None:
            request.user.benefactor.first_name = request.POST.get("first_name")
        if request.POST.get("last_name") is not None:
            request.user.benefactor.last_name = request.POST.get("last_name")
        if request.POST.get("gender") is not None:
            request.user.benefactor.gender = request.POST.get("gender")
        if request.POST.get("age") is not None:
            request.user.benefactor.age = request.POST.get("age")
        request.user.benefactor.save()
    Logger.account_update(request.user, None, None)
    # TODO Fix Redirect
    return HttpResponseRedirect(reverse('accounts:user_profile'))

    # if not request.user.is_authenticated :
    # return 1 #fixme redirect to error.html with appropriate context


@csrf_exempt
def add_benefactor_credit(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = error_context_generate('Authentication Error', 'You are not Signed In!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not request.user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_charity:
        # TODO Raise Account Type Error
        context = error_context_generate('Account Type Error',
                                         'I Don\'t Know How You Ended Here But Charities Cannot Add Credits!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    # try:
    benefactor = get_object(Benefactor, user=request.user)
    amount = int(request.POST.get('deposit_amount'))
    benefactor.credit += amount
    benefactor.save()
    # FIXME Redirect to user profile view
    Logger.account_update(request.user, None, None)
    return HttpResponseRedirect(reverse('user_profile'))
    # except:
    #     context = {
    #         'error_message': 'error in deposit!',
    #         # FIXME Redirect to user profile view
    #         'redirect_address': 'user_profile'
    #     }
    #     return HttpResponseRedirect(reverse('error'))


def submit_benefactor_comment(request, benefactor_username):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = error_context_generate('Authentication Error', 'You are not Signed In!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not request.user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_benefactor:
        # TODO Raise Account Type Error
        context = error_context_generate('Account Type Error', 'Benefactors Cannot Comment on Other Benefactors', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    benefactor_users = User.objects.filter(username=benefactor_username)
    if benefactor_users.count() <= 0:
        # TODO Raise Not Found Error
        context = error_context_generate('Not Found', 'Requested User Cannot be Found', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    benefactor_user = benefactor_users.all()[0]
    try:
        benefactor = get_object(Benefactor, user=get_object(User, username=benefactor_username))
        if request.user.charity.benefactor_history.filter(user=benefactor.user).count() <= 0:
            context = error_context_generate('No Cooperation Error',
                                             'You Cannot Submit Score for a Benefactor with Whom You Had no Cooperation!',
                                             '')
            # TODO Raise No_Cooperation Error
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        comment = BenefactorComment.objects.create(commented=benefactor_user.benefactor, commentor=request.user.charity,
                                                   comment_string=request.POST.get('comment_string'))
        # TODO Redirect to Benefactor Profile Page
        Logger.submit_comment(request.user, benefactor.user, None)
        return HttpResponseRedirect([])
    except:
        # TODO Raise Unexpcted Error
        context = error_context_generate('Unexpected Error', 'Error While Submitting The Comment', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def submit_charity_commit(request, charity_username):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = error_context_generate('Authentication Error', 'You are not Signed In!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not request.user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_charity:
        # TODO Raise Account Type Error
        context = error_context_generate('Account Type Error', 'Charities Cannot Comment on Other Charities', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.benefactor.charity_set.get(user=get_object(User, username=charity_username)).count <= 0:
        context = error_context_generate('No Cooperation Error',
                                         'You Cannot Submit Score for a Charity with Which You Had no Cooperation!', '')
        # TODO Raise No_Cooperation Error
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    charity_users = User.objects.filter(username=charity_username)
    if charity_users.count() <= 0:
        # TODO Raise Not Found Error
        context = error_context_generate('Not Found', 'Requested User Cannot be Found', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    charity_user = charity_users.all()[0]
    try:
        comment = CharityComment.objects.create(commented=charity_user.charity, commentor=request.user.benefactor,
                                                comment_string=request.POST.get('comment_string'))
        # TODO Redirect to Charity Profile Page
        Logger.account_update(request.user, charity_user, None)
        return HttpResponseRedirect([])
    except:
        # TODO Raise Unexpected Error
        context = error_context_generate('Unexpected Error', 'Error While Submitting The comment', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def error_redirect(request, redirect_address):
    return HttpResponseRedirect(reverse(redirect_address))


class ErrorView(TemplateView):
    template_name = 'accounts/error_page.html'


def logout_user(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = error_context_generate('Authentication Error', 'You are not Signed In!', 'accounts:login_view')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    Logger.logout(request.user, None, None)
    logout(request)
    template = loader.get_template('accounts/login.html')
    return HttpResponse(template.render(request, {}))

