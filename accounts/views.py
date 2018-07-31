from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
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
from projects.models import CooperationRequest


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
        context = {
            'error_message': 'Authentication Error: You Don\'t Have Permission to Change this Account!'
        }
        pass

    ability_type_name = request.POST.get('add_ability_ability_type_name')
    ability_description = request.POST.get('add_ability_description')
    ability_type = AbilityType.objects.all().filter(name__iexact=ability_type_name)[0]
    benefactor = Benefactor.objects.all().filter(user_id=benefactor_id)[0]
    ability = Ability(benefactor=benefactor, ability_type=ability_type, description=ability_description)
    ability.save()
    benefactor.ability_set.add(ability)
    # TODO Fix Path
    return HttpResponseRedirect('path')


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
    charities = Charity.objects.all()
    # FIXME fix url
    return render(request, 'url', {
        'all_charities': list(charities)
    })


def admin_get_benefactors(request):
    benefactors = Benefactor.objects.all()
    # FIXME fix url
    return render(request, 'url', {
        'all_benefactors': list(benefactors)
    })


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


def submit_benefactor_score(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = {
            'error_message': 'Authentication Error: You are not Signed In!'
        }
        return HttpResponse([])
    if request.user.is_benefactor:
        # TODO Raise Account Type Error
        context = {
            'error_message': 'Account Type Error: You Can\'t Submit Score for Another Benefactor!'
        }
        return HttpResponse([])
    charity = Charity.objects.get(user=request.user)
    benefactor = Benefactor.objects.get(user=User.objects.get(username=request.POST.get('benefactor_username')))
    if charity.benefactor_history.filter(user=benefactor.user).count() <= 0:
        context = {
            'error_message': ' No Cooperation Error: You Cannot Submit Score for a Benefactor with Whom You Had no Cooperation!'
        }
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
        context = {
            'error_message': 'UnExpected Error: Some of the Data Needed for The Page is Lost or Damaged'
        }
        return HttpResponse([])
        # TODO raise error


def submit_charity_score(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = {
            'error_message': 'Authentication Error: You are not Signed In!'
        }
        return HttpResponse([])
    if request.user.is_charity:
        context = {
            'error_message': 'Account Type Error: You Can\'t Submit Score for Another Charity!'
        }
        # TODO Raise Account Type Error
        return HttpResponse([])
    benefactor = Benefactor.objects.get(user=request.user)
    if benefactor.charity_set.get(user=User.objects.get(username=request.POST.get('charity_username'))).count <= 0:
        context = {
            'error_message': ' No Cooperation Error: You Cannot Submit Score for a Charity with Which You Had no Cooperation!'
        }
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
        context = {
            'error_message': 'UnExpected Error: Some of the Data Needed for The Page is Lost or Damaged'
        }
        return HttpResponse([])


def submit_ability_request(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = {
            'error_message': 'Authentication Error: You are not Signed In!'
        }
        return HttpResponse([])
    try:
        new_request = AbilityRequest.objects.create(type=request.POST.get('type'), name=request.POST.get('name'),
                                                    description=request.POST.get('description'))
        new_request.save()
        return HttpResponseRedirect([])
    except:
        # TODO Raise Error
        context = {
            'error_message': 'UnExpected Error: Some of the Data Needed for The Page is Lost or Damaged'
        }
        return HttpResponse([])


def submit_cooperation_request(request, project_id):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = {
            'error_message': 'Authentication Error: You are not Signed In!'
        }
        return HttpResponse([])
    try:
        # FIXME How should we find the project? I mean which data is given to find the project with?
        project = NonFinancialProject.objects.all().filter(project_id=project_id)
        if request.user.is_benefactor:
            benefactor = Benefactor.objects.get(user=request.user)
            charity = Charity.objects.get(user=User.objects.get(username=request.POST.get('username')))
            new_notification = Notification.objects.create(type='new_request',user=charity.user, datetime=datetime.datetime.now())
            new_notification.description = 'A new Cooperation Request is Received for Project ' + project.project
            new_notification.save()
            request_type = 'b2c'
        else:
            benefactor = Benefactor.objects.get(user=User.objects.get(username=request.POST.get('username')))
            charity = Charity.objects.get(user=request.user)
            new_notification = Notification.objects.create(type='new_request',user=benefactor.user, datetime=datetime.datetime.now())
            new_notification.description = 'A new Cooperation Request Has Been Received!'
            new_notification.save()
            request_type = 'c2b'
        new_request = CooperationRequest.objects.create(benefactor=benefactor, charity=charity, type=request_type,
                                                        description=request.POST.get('description'))
        new_request.nonfinancialproject = project
        new_request.save()
        return HttpResponseRedirect([])
    except:
        # TODO Raise Error
        context = {
            'error_message': 'UnExpected Error: Some of the Data Needed for The Page is Lost or Damaged'
        }
        return HttpResponse('error')


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
    try:

        test1_user = User.objects.filter(username=request.POST.get("username"))
        test2_user = User.objects.filter(username=request.POST.get("email"))
        if test1_user.__len__() != 0 and test2_user.__len__() != 0:

            return render(request, 'accounts/register.html', {'error_message': 'Account already exists! Try login or forget password.'})

        if test1_user.__len__() == 0 and len(test2_user) != 0:
            return render(request, 'accounts/register.html', {'error_message': 'Email is already taken!  '})

        if len(test1_user) != 0 and len(test2_user) == 0:
            return render(request, 'accounts/register.html', {'error_message': 'Username is already taken! try another username.  '})




        tmp_contact_info = ContactInfo.objects.create(country="Iran",
                                                      province=request.POST.get("province"),
                                                      city=request.POST.get("city"),
                                                      address=request.POST.get("address"),
                                                      postal_code=request.POST.get("postal_code"),
                                                      phone_number=request.POST.get("phone_number")
                                                      )
        tmp_user = User.objects.create(username=request.POST.get("username"),
                                       password=request.POST.get("password"),
                                       email=request.POST.get("email"),
                                       contact_info=tmp_contact_info
                                       )

        tmp_user.save()
        if request.POST.get("account_type") == "Charity":
            tmp_user.is_charity = True
            tmp_charity = Charity.objects.create(user=tmp_user, name=request.POST.get("charity_name"), score=-1)
            tmp_charity.save()
            tmp_user.save()

            login(request, tmp_user)
            return render(request, 'accounts/charity.html')


        else:
            tmp_user.is_benefactor = True
            tmp_benefactor = Benefactor.objects.create(user=tmp_user, first_name=request.POST.get("first_name"),
                                                       last_name=request.POST.get("last_name"), score=-1,
                                                       age=request.POST.get("age"), gender=request.POST.get('gender'))
            tmp_benefactor.save()
            tmp_user.save()
            login(request, tmp_user)
            return render(request, 'accounts/user-profile.html')

    except:
        context = {
            'error_message': 'Sign Up Error!',
            'redirect_address': 'signup_view'
        }
        return render(request, 'accounts/register.html', context)


####Login

class LoginView(TemplateView):
    template_name = "accounts/login.html"


@csrf_exempt
def login_user(request):
    # tmp_user = get_object_or_404(User,username=request.POST.get("username"),password=request.POST.get("password"))
    try:
        tmp_user = User.objects.filter(username=request.POST.get("username"))
        if len(tmp_user) == 0:
            return render(request, 'accounts/login.html')
        tmp_user = User.objects.get(username=request.POST.get("username"))
        if tmp_user.password != request.POST.get("password"):
            return render(request, 'accounts/login.html', {'error_msg': 'Invalid password -.-'})

        if tmp_user.is_charity:

            login(request, user=tmp_user)
            return render(request, 'accounts/charity.html')

        else:

            login(request, tmp_user)
            return render(request, 'accounts/user-profile.html')
    except:

        context = {
            'error_message': "Username or Password is Invalid!!!!!",
            'redirect_address': "login_view"

        }
        template = loader.get_template('accounts/login.html')

        return HttpResponse(template.render(context, request))


def user_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html', {'error_message': 'please login first'})
    try:
        print(request.user)
        context = {"type": request.user.is_charity, "username": request.user.username, "email": request.user.email,
                   "country": request.user.contact_info.country, "province": request.user.contact_info.province,
                   "city": request.user.contact_info.city, "address": request.user.contact_info.address,
                   "phone_number": request.user.contact_info.phone_number}
        if request.user.is_benefactor:
            # try:
                benefactor = Benefactor.objects.get(user=request.user)
                context['user'] = benefactor
                context['benefactor'] = benefactor
                projects = {project for project in Project.objects.all() if benefactor in project.benefactors}
                context['project_count'] = len(projects)
                abilities = benefactor.ability_set.all()
                if benefactor.score == -1:
                    score = 'N/A'
                else:
                    score = 0
                    for ability in abilities:
                        score += ability.score
                    score /= abilities
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
                charity = Charity.objects.get(user=request.user)
                context["name"] = charity.name
                context["score"] = charity.score
            except:
                print(1)
        return render(request, 'accounts/user-profile.html', context)
    except:
        context = {
            'error_message': 'Error Getting Account Data!'
        }
        # TODO Raise Error
        return HttpResponseRedirect([])


#### Customize User

@csrf_exempt
def customize_user_data(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html', {'error_message': 'please login first'})
    if request.method == 'GET':
        return render(request, 'accounts/user-profile.html')
    try:
        notifications = Notification.objects.filter(user=request.user).all()
        context = {"type": request.user.is_charity, "username": request.user.username, "email": request.user.email,
                   "country": request.user.contact_info.country, "province": request.user.contact_info.province,
                   "city": request.user.contact_info.city, "address": request.user.contact_info.address,
                   "phone_number": request.user.contact_info.phone_number,"description": request.user.description,
                   "notifications": notifications}
        if request.user.is_benefactor:
            try:
                benefactor = Benefactor.objects.get(user=request.user)
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
        context = {
            'error_message': 'Error Getting Account Data!'
        }
        # TODO Raise Error
        return HttpResponseRedirect([])


def customize_user(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = {
            'error_message': 'Authentication Error: You are not Signed In!'
        }
        return HttpResponse([])
    request.user.password = request.POST.get("password")
    request.user.description = request.POST.get("description")
    if request.POST.get("province") is not None:
        request.user.contact_info.province = request.POST.get("province")
    if request.POST.get("city") is not None:
        request.user.contact_info.city = request.POST.get("city")
    request.user.contact_info.address = request.POST.get("address")
    request.user.contact_info.phone_number = request.POST.get("phone_number")
    request.user.save()
    if request.user.is_charity:
        request.user.charity.name = request.POST.get("name")
        request.user.charity.save()
    else:
        request.user.benefactor.first_name = request.POST.get("first_name")
        request.user.benefactor.last_name = request.POST.get("last_name")
        request.user.benefactor.gender = request.POST.get("gender")
        request.user.benefactor.age = request.POST.get("age")
        request.user.benefactor.save()

    return render(request, '', )


    # if not request.user.is_authenticated :
    # return 1 #fixme redirect to error.html with appropriate context


@csrf_exempt
def add_benefactor_credit(request):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = {
            'error_message': 'Authentication Error: You are not Signed In!'
        }
        return HttpResponse([])
    if request.user.is_charity:
        # TODO Raise Account Type Error
        context = {
            'error_message': 'Account Type Error: I Don\'t Know How You Ended Here But Charities Cannot Add Credits!'
        }
        return HttpResponse([])
    # try:
    benefactor = Benefactor.objects.get(user=request.user)
    amount = int(request.POST.get('deposit_amount'))
    benefactor.credit += amount
    benefactor.save()
    # FIXME Redirect to user profile view
    return render(request, 'accounts/user-profile.html')
    # except:
    #     context = {
    #         'error_message': 'error in deposit!',
    #         # FIXME Redirect to user profile view
    #         'redirect_address': 'user_profile'
    #     }
    #     return HttpResponseRedirect(reverse('error'))

