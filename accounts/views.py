from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.template import loader

from projects.models import NonFinancialProject, Project
from accounts.models import *



####### Danial imports .Some of them may be redundant!!! 

from django.contrib.auth import login
from django.shortcuts import redirect,get_object_or_404
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader

from accounts.forms import CharitySignUpForm
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
        new_request.nonfinancialproject=project
        new_request.save()
        return HttpResponseRedirect([])
    except:
        # TODO Raise Error
        return HttpResponse('error')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#################################################################
#################################################################
#################################################################
#ignore this block



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
    template_name = "registration/signup.html"



def signup(request):

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
    if  request.POST.get("account_type") == "Charity":
        tmp_user.is_charity = True
        tmp_charity= Charity.objects.create(user=tmp_user,name=request.POST.get("charity_name"),score=-1)
        tmp_charity.save()




    else :
        tmp_user.is_charity = True
        tmp_benefactor= Benefactor.objects.create(user=tmp_user,first_name=request.POST.get("first_name"),last_name=request.POST.get("last_name"),score=-1,age=request.POST.get("age"))
        tmp_benefactor.save()




    login(request, tmp_user)
    return HttpResponseRedirect(reverse("Home"))




####Login

class LoginView(TemplateView):
    template_name = "registration/login.html"


def login_user(request):

   # tmp_user = get_object_or_404(User,username=request.POST.get("username"),password=request.POST.get("password"))
    try:
        tmp_user = User.objects.get(username=request.POST.get("username"))
        if tmp_user.password != request.POST.get("password") :
            raise Exception


        if  tmp_user.is_charity :

            login(request,user=tmp_user)
            return HttpResponseRedirect(reverse("Home"))

        else:

            login(request, tmp_user)
            return HttpResponseRedirect(reverse("Home"))
    except:


        context = {
            'error_message':"Username or Password is Invalid!!!!!",
            'redirect_address':"login_view"

        }
        template = loader.get_template('error.html')

        return HttpResponse(template.render(context, request))


#### Customize User

class CustomizeUserView(TemplateView):
    template_name = "registration/customize_user.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["type"]=self.request.user.is_charity
        context["username"]=self.request.user.username
        context["email"]=self.request.user.email

        context["country"]=self.request.user.contact_info.country
        context["province"] = self.request.user.contact_info.province
        context["city"] = self.request.user.contact_info.city
        context["address"] = self.request.user.contact_info.address
        context["phone_number"]=self.request.user.contact_info.phone_number

        if self.request.user.is_benefactor :
            try:
                context["first_name"] = self.request.user.benefactor.first_name
                context["last_name"]  = self.request.user.benefactor.last_name
                context["gender"] = self.request.user.benefactor.gender
                context["age"] = self.request.user.benefactor.age
            except:
                print(1)


        else:
            try :
                context["name"] = self.request.user.charity.name
            except:
                print(1)



        return context



def customize_user(request):


    request.user.contact_info.province = request.POST.get("province")
    request.user.contact_info.city = request.POST.get("city")
    request.user.contact_info.address = request.POST.get("address")
    request.user.contact_info.phone_number = request.POST.get("phone_number")

    if request.user.is_charity:

        request.user.charity.name = request.POST.get("name")
    else:
        request.user.benefactor.first_name = request.POST.get("first_name")
        request.user.benefactor.last_name = request.POST.get("last_name")
        request.user.benefactor.gender = request.POST.get("gender")
        request.user.benefactor.age = request.POST.get("age")

    return HttpResponseRedirect(reverse("Home"))


   # if not request.user.is_authenticated :
        #return 1 #fixme redirect to error.html with appropriate context




