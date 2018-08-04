from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from AZED.views import check_valid
from accounts.log_util import create_financial_project_report, create_non_financial_project_report, Logger
from accounts.models import AbilityTag, Notification
from accounts.search_util import create_query_schedule
from projects.models import *
from django.template import loader


def get_object(obj_class, *args, **kwargs):
    try:
        obj_set = obj_class.objects.filter(*args, **kwargs)
        if obj_set.count() <= 0:
            return None
        return obj_set.all()[0]
    except:
        # TODO Raise Super Ultra Exceptional Error
        return 'Error'


def error_context_generate(error_title, error_message, redirect_address):
    return {
        'error_title': error_title,
        'error_message': error_message,
        'redirect_address': redirect_address
    }


def sign_in_error():
    return error_context_generate('Authentication Error', 'You Are Not Signed In!', '')


# Create your views here.

@csrf_exempt
def find_non_financial_projects_advanced_search_results(request):
    if not request.user.is_authenticated:
        # TODO Raise Auth Error
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_charity:
        pass
    all_ability_types = [ability_type.name for ability_type in AbilityType.objects.all()]
    all_ability_tags = [ability_tag.name for ability_tag in AbilityTag.objects.all()]

    if request.method == 'GET':
        return render(request, 'projects/non-fin-advanced-search', {
            'ability_types': all_ability_types,
            'ability_tags': all_ability_tags,
            'result_non_financial_projects': []
        })

    project_name = request.POST.get('search_non_financial_project_name')
    charity_name = request.POST.get('search_non_financial_charity_name')
    benefactor_name = request.POST.get('search_non_financial_benefactor_name')
    project_state = request.POST.get('search_non_financial_project_state')
    ability_name = request.POST.get('search_non_financial_ability_name')
    tags = request.POST.get('search_non_financial_tags')
    start_date = convert_str_to_date(request.POST.get('search_non_financial_start_date'))
    end_date = convert_str_to_date(request.POST.get('search_non_financial_end_date'))
    weekly_schedule = create_query_schedule(request.POST.get('search_non_financial_schedule'))
    schedule = [start_date, end_date, weekly_schedule]
    min_required_hours = request.POST.get('searchnon_financial_min_required_hours')
    min_required_hours = None if min_required_hours is None else float(min_required_hours)
    min_date_overlap = request.POST.get('search_non_financial_min_date_overlap')
    min_date_overlap = None if min_date_overlap is None else float(min_date_overlap)
    min_time_overlap = request.POST.get('search_non_financial_min_time_overlap')
    min_time_overlap = None if min_time_overlap is None else float(min_time_overlap)
    age = request.POST.get('search_non_financial_age')
    age = None if age is None else int(age)
    gender = request.POST.get('search_non_financial_gender')
    country = request.POST.get('search_non_financial_country')
    province = request.POST.get('search_non_financial_province')
    city = request.POST.get('search_non_financial_city')
    project_queryset = search_non_financial_project(project_name, charity_name, benefactor_name, project_state,
                                                    ability_name, tags, schedule, min_required_hours, min_date_overlap,
                                                    min_time_overlap, age, gender, country, province, city)
    return render(request, 'projects/non-fin-advanced-search', {
        'result_non_financial_projects': list(project_queryset),
        'ability_types': all_ability_types,
        'ability_tags': all_ability_tags
    })


@csrf_exempt
def find_non_financial_projects_search_results(request):
    if not request.user.is_authenticated:
        # TODO Raise Auth Error
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_charity:
        # TODO Raise Account Type Error
        context = error_context_generate('Account Type Error', 'Charities Cannot Search for Projects', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    all_ability_types = [ability_type.name for ability_type in AbilityType.objects.all()]
    all_ability_tags = [ability_tag.name for ability_tag in AbilityTag.objects.all()]

    if request.method == 'GET':
        return render(request, 'projects/non-fin-search', {
            'ability_types': all_ability_types,
            'ability_tags': all_ability_tags,
            'result_non_financial_projects': []
        })

    project_name = request.POST.get('search_non_financial_project_name')
    charity_name = request.POST.get('search_non_financial_charity_name')
    benefactor_name = request.POST.get('search_non_financial_benefactor_name')
    project_state = request.POST.get('search_non_financial_project_state')
    ability_name = request.POST.get('search_non_financial_ability_name')
    tags = request.POST.get('search_non_financial_tags')
    start_date = convert_str_to_date(request.POST.get('search_non_financial_start_date'))
    end_date = convert_str_to_date(request.POST.get('search_non_financial_end_date'))
    weekly_schedule = create_query_schedule(request.POST.get('search_non_financial_schedule'))
    schedule = [start_date, end_date, weekly_schedule]
    min_required_hours = request.POST.get('searchnon_financial_min_required_hours')
    min_required_hours = None if min_required_hours is None else float(min_required_hours)
    min_date_overlap = request.POST.get('search_non_financial_min_date_overlap')
    min_date_overlap = None if min_date_overlap is None else float(min_date_overlap)
    min_time_overlap = request.POST.get('search_non_financial_min_time_overlap')
    min_time_overlap = None if min_time_overlap is None else float(min_time_overlap)
    age = request.POST.get('search_non_financial_age')
    age = None if age is None else int(age)
    gender = request.POST.get('search_non_financial_gender')
    country = request.POST.get('search_non_financial_country')
    province = request.POST.get('search_non_financial_province')
    city = request.POST.get('search_non_financial_city')
    project_queryset = search_non_financial_project(project_name, charity_name, benefactor_name, project_state,
                                                    ability_name, tags, schedule, min_required_hours, min_date_overlap,
                                                    min_time_overlap, age, gender, country, province, city)
    return render(request, 'projects/non-fin-search', {
        'result_non_financial_projects': list(project_queryset),
        'ability_types': all_ability_types,
        'ability_tags': all_ability_tags
    })


@csrf_exempt
def find_financial_project_search_results(request):
    if not request.user.is_authenticated:
        # TODO Raise Auth Error
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_charity:
        context = error_context_generate('Account Type Error', 'Charities Cannot Search for Projects', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    project_name = request.POST.get('search_financial_project_name')
    charity_name = request.POST.get('search_financial_charity_name')
    benefactor_name = request.POST.get('search_financial_benefactor_name')
    project_state = request.POST.get('search_financial_project_state')
    min_progress = request.POST.get('search_financial_min_progress')
    min_progress = None if min_progress is None else float(min_progress)
    max_progress = request.POST.get('search_financial_max_progress')
    max_progress = None if max_progress is None else float(max_progress)
    min_deadline_date = convert_str_to_date(request.POST.get('search_financial_min_deadline_date'))
    max_deadline_date = convert_str_to_date(request.POST.get('search_financial_max_deadline_date'))
    project_queryset = search_financial_project(project_name, charity_name, benefactor_name, project_state,
                                                min_progress, max_progress, min_deadline_date, max_deadline_date)
    return render(request, 'url', {'result_financial_projects': list(project_queryset)})


@csrf_exempt
def find_charity_search_results(request):
    if not request.user.is_authenticated:
        # TODO Raise Auth Error
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_charity:
        context = error_context_generate('Account Type Error', 'Charities Cannot Search for Projects', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    charity_name = request.POST.get('search_charity_name')
    min_score = request.POST.get('search_charity_min_score')
    min_score = None if min_score is None else float(min_score)
    max_score = request.POST.get('search_charity_max_score')
    max_score = None if max_score is None else float(max_score)
    min_related_projects = request.POST.get('search_charity_min_related_projects')
    min_related_projects = None if min_related_projects is None else int(min_related_projects)
    max_related_projects = request.POST.get('search_charity_max_related_projects')
    max_related_projects = None if max_related_projects is None else int(max_related_projects)
    min_finished_projects = request.POST.get('search_charity_min_finished_projects')
    min_finished_projects = None if min_finished_projects is None else int(min_finished_projects)
    max_finished_projects = request.POST.get('search_charity_max_finished_projects')
    max_finished_projects = None if max_finished_projects is None else int(max_finished_projects)
    benefactor_name = request.POST.get('search_charity_benefactor_name')
    country = request.POST.get('search_charity_country')
    province = request.POST.get('search_charity_province')
    city = request.POST.get('search_charity_city')
    charity_queryset = search_charity(charity_name, min_score, max_score, min_related_projects, max_related_projects,
                                      min_finished_projects, max_finished_projects, benefactor_name, country, province,
                                      city)
    return render(request, 'url', {'result_charities': list(charity_queryset)})


@csrf_exempt
# TODO handle security and stuff like that
def find_benefactor_search_results(request):
    if not request.user.is_authenticated:
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_benefactor:
        context = error_context_generate('Account Type Error', 'Benefactors Cannot Search for Other Benefactors', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    start_date = convert_str_to_date(request.POST.get('search_benefactor_start_date'))
    end_date = convert_str_to_date(request.POST.get('search_benefactor_end_date'))
    weekly_schedule = create_query_schedule(request.POST.get('search_benefactor_schedule'))
    schedule = [start_date, end_date, weekly_schedule]
    min_required_hours = request.POST.get('search_benefactor_min_required_hours')
    min_required_hours = None if min_required_hours is None else float(min_required_hours)
    min_date_overlap = request.POST.get('search_benefactors_min_date_overlap')
    min_date_overlap = None if min_date_overlap is None else float(min_date_overlap)
    min_time_overlap = request.POST.get('search_benefactors_min_time_overlap')
    min_time_overlap = None if min_time_overlap is None else float(min_time_overlap)
    tags = request.POST.get('search_benefactor_tags')
    ability_name = request.POST.get('search_benefactor_ability_name')
    ability_min_score = request.POST.get('search_benefactor_ability_min_score')
    ability_min_score = None if ability_min_score is None else float(ability_min_score)
    ability_max_score = request.POST.get('search_benefactor_ability_max_score')
    ability_max_score = None if ability_max_score is None else float(ability_max_score)
    country = request.POST.get('search_benefactor_country')
    province = request.POST.get('search_benefactor_province')
    city = request.POST.get('search_benefactor_city')
    user_min_score = request.POST.get('search_benefactor_user_min_score')
    user_min_score = None if user_min_score is None else float(user_min_score)
    user_max_score = request.POST.get('search_benefactor_user_max_score')
    user_max_score = None if user_max_score is None else float(user_max_score)
    gender = request.POST.get('search_benefactor_gender')
    first_name = request.POST.get('search_benefactor_first_name')
    last_name = request.POST.get('search_benefactor_last_name')
    result_benefactor_data = search_benefactor(schedule, min_required_hours, min_date_overlap, min_time_overlap, tags,
                                               ability_name, ability_min_score, ability_max_score, country, province,
                                               city, user_min_score, user_max_score, gender, first_name, last_name)
    # benefactor_list = list(benefactor_queryset)
    # result_benefactor_data = []
    # for benefactor, overlap_data in zip(benefactor_list, search_overlap_data):
    #     result_benefactor_data.append([benefactor, overlap_data[0], overlap_data[1]])

    return render(request, 'wtf?', {'result_benefactors': result_benefactor_data})


@csrf_exempt
def create_new_project(request):
    if request.method == 'GET':
        projects = request.user.charity.project_set
        return render(request, 'accounts/create-project.html', {'result_set': projects})
    if request.user.is_authenticated:
        if not request.user.is_active:
            context = error_context_generate('Deactivated Account Error',
                                             'Your Account Has Been Marked as Deactivated!', '')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        project = Project.objects.create()
        project.project_name = request.POST.get('project_name')
        project.charity = request.user
        project.description = request.POST.get('description')
        project.state = 'open'
        project.save()
        if request.POST.get('type') is 'financial':
            project.type = 'financial'
            financial_project = FinancialProject.objects.create()
            if request.POST.get('start_date') is not None:
                financial_project.start_date = datetime.datetime.strptime(request.POST.get('start_date'), '%y-%m-%d')
            else:
                financial_project.start_date = datetime.date.today()
            # FIXME only date not datetime?
            financial_project.end_date = datetime.datetime.strptime(request.POST.get('end_date'), '%y-%m-%d')
            financial_project.project = project
            financial_project.target_money = float(request.POST.get('target_money'))
            if request.POST.get('current_money') is not None:
                financial_project.current_money = float(request.POST.get('current_money'))
            else:
                financial_project.current_money = 0
            financial_project.save()

        else:
            project.type = 'non-financial'
            non_financial_project = NonFinancialProject.objects.create()
            non_financial_project.project = project
            if check_valid(request.POST.get("ability_type")):
                non_financial_project.ability_type = request.POST.get("ability_type")
            if check_valid(request.POST.get("min_age")):
                non_financial_project.min_age = int(request.POST.get("min_age"))
            if check_valid(request.POST.get("max_age")):
                non_financial_project.max_age = int(request.POST.get("max_age"))
            non_financial_project.required_gender = request.POST.get("required_gender")

            non_financial_project.country = request.POST.get("country")
            non_financial_project.province = request.POST.get("province")
            non_financial_project.city = request.POST.get("city")
            date_interval = DateInterval.objects.create()
            date_interval.begin_date = convert_str_to_date(request.POST.get('start_date'))
            date_interval.end_date = convert_str_to_date(request.POST.get('end_date'))
            date_interval.non_financial_project = non_financial_project
            # FIXME check if the input is JSON or not
            date_interval.to_json(create_query_schedule(request.POST.get('week_schedule')))
            non_financial_project.save()
        projects = request.user.charity.project_set
        Logger.create_new_project(request.user, None, project)
        # TODO Fix redirect path
        return render(request, 'accounts/create-project.html', {'result_set': projects})
    else:
        # TODO Fix content
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


def edit_project(request, pk):
    # TODO fix path
    template = loader.get_template('path-to-template')
    if not request.user.is_authenticated:
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.method != 'POST':
        context = error_context_generate('Connection Error', 'Request Method is not POST!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    project = get_object(Project, pk=pk)
    try:
        dic = request.POST
        project.project_name = dic['project_name']
        project.project_state = dic['project_state']
        project.description = dic['description']
        if project.type is 'financial':
            fin_project = get_object(FinancialProject, project=project)
            fin_project.target_money = dic['target_money']
            fin_project.start_date = convert_str_to_date(dic['start_date'])
            fin_project.end_date = convert_str_to_date(dic['end_date'])
            # FIXME should the current_money be editable or not?
            fin_project.current_money = dic['current_money']
            fin_project.save()
        else:
            nf_project = get_object(NonFinancialProject, project=project)
            nf_project.ability_type = dic['ability_type']
            nf_project.city = dic['city']
            nf_project.country = dic['country']
            nf_project.max_age = dic['max_age']
            nf_project.min_age = dic['min_age']
            nf_project.project = dic['province']
            nf_project.required_gender = dic['required_gender']
            date_interval = nf_project.dateinterval
            if check_valid(dic.get('start_date')):
                date_interval.begin_date = convert_str_to_date(dic['start_date'])
            date_interval.end_date = convert_str_to_date(dic['end_date'])
            if check_valid(dic.get('week_schedule')):
                date_interval.to_json(create_query_schedule(dic['week_schedule']))
            nf_project.save()
            date_interval.save()
        project.save()
        Logger.update_project(request.user, None, project)
    except:
        context = {
            'pk': pk,
            'error_message': 'Error in finding the Project!'
        }
        context = error_context_generate('Unexpected Error', 'Some of the Required Files Are Damaged or Lost!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    # FIXME maybe all responses should be Redirects / parameters need fixing
    return HttpResponseRedirect([])


def show_project_data(request, pid):
    projects = Project.objects.filter(id=pid)
    if len(projects) <= 0:
        # TODO Raise 404
        context = error_context_generate('Not Found', 'Cannot Find the Requested Project', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    project = projects[0]
    # TODO fix template path
    template = loader.get_template('projects/get_project_data_for_edit.html')
    try:
        owner = request.user.is_charity and project.charity.user is request.user
        context = {
            'project': project,
            'is_owner': owner,

        }
        if project.type is 'financial':
            fin_project = get_object(FinancialProject, project=project)
            contributions = FinancialContribution.objects.filter(financial_project=fin_project)
            context.update({
                'start_date': fin_project.start_date,
                'end_date': fin_project.end_date,
                'target_money': fin_project.target_money,
                'current_money': fin_project.current_money,
                'contributions': contributions.all(),
            })
        else:
            nf_project = get_object(NonFinancialProject, project=project)
            date_interval = get_object(DateInterval, non_financial_project=nf_project)
            helper = nf_project.project.benefactors
            b_username = None
            b_fullname = None
            if not helper.count() <= 0:
                # Error Prone Line
                b_username = helper.all()[0].user.username
                b_fullname = helper.all()[0].first_name + ' ' + helper.all()[0].last_name
            context.update({
                'ability_type': nf_project.ability_type,
                'min_age': nf_project.min_age,
                'max_age': nf_project.max_age,
                'required_gender': nf_project.required_gender,
                'country': nf_project.country,
                'province': nf_project.province,
                'city': nf_project.city,
                'start_date': date_interval.begin_date,
                'end_date': date_interval.end_date,
                'b_username': b_username,
                'b_fullname': b_fullname,
            })
    except:
        context = error_context_generate('Unexpected Error', 'Some of the Required Files Are Damaged or Lost!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    return HttpResponse(template.render(context, request))


class CreateProjectForm(TemplateView):
    template_name = "accounts/create-project.html"


@csrf_exempt
def contribute_to_project(request, project_id):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not request.user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_charity:
        # TODO Raise Account Type Error
        context = error_context_generate('Account Type', 'Charities Cannot Contribute to Other Charities\' Projects',
                                         '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    project = get_object(Project, id=project_id)
    if project.type != 'financial':
        # TODO Raise Project Type Error
        context = error_context_generate('Project Type', 'Project Type is Not Financial', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    fin_project = get_object(FinancialProject, project=project)
    try:
        if project.project_state is 'completed':
            # TODO Raise Project Closed Error
            context = error_context_generate('Project Closed', 'Project is Already Closed', '')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        amount = float(request.POST.get('money'))
        benefactor = get_object(Benefactor, user=request.user)
        if benefactor.credit < amount:
            # TODO Raise Not Enough Money Error
            context = error_context_generate('Low Credits', 'Your Account\'s Credits is not Enough', '')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        contribution = get_object(FinancialContribution, benefactor=benefactor, financial_project=fin_project)
        if contribution is not None:
            contribution.money += amount
            contribution.save()
        else:
            FinancialContribution.objects.create(benefactor=benefactor, financial_project=fin_project, money=amount)
        benefactor.credit -= amount
        fin_project.add_contribution(amount)
        benefactor.save()
        new_notification = Notification.objects.create(type='project_contribution', user=project.charity.user,
                                                       datetime=datetime.datetime.now())
        new_notification.description = str(amount) + ' Has been Contributed to Project ' + project
        if fin_project.project.project_state is 'completed':
            new_notification.description += '\n Project Has Been Completed Successfully!'
        new_notification.save()
        Logger.financial_contribution(request.user, project.charity, project)
        # TODO Redirect
        return HttpResponseRedirect([])
    except:
        # TODO Raise Unexpected Error
        context = error_context_generate('Unexpected Error', 'Some Required Files are Lost or Damaged!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


@csrf_exempt
def get_project_report(request, project_id):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not request.user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if request.user.is_benefactor:
        # TODO Raise Account Type Error
        context = error_context_generate('Account Type Error', 'Benefactors Cannot Get Reports on Projects', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    project = get_object(Project, id=project_id)
    charity = get_object(Charity, user=request.user)
    try:
        if project.charity != charity:
            # TODO Raise Owner Error
            context = error_context_generate('Owner Error', 'You Are Not The Owner of The Project', '')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        if project.type is 'financial':
            fin_project = get_object(FinancialProject, project=project)
            context = {'report': create_financial_project_report(fin_project),
                       'project_id': project_id}
            # TODO Return Context
            return HttpResponse(context)
        else:
            nf_project = get_object(NonFinancialProject, project=project)
            context = {
                'report': create_non_financial_project_report(nf_project),
                'project_id': project_id
            }
            # TODO Return Context
            return HttpResponse(context)
    except:
        # TODO Raise Unexpected Error
        context = error_context_generate('Unexpected Error', 'Some Required Files are Lost or Damaged!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))


@csrf_exempt
def accept_request(request, rid):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not request.user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        req = get_object(CooperationRequest, id=rid)
        benefactor = req.benefactor
        charity = req.charity
        if req.state is 'closed':
            # TODO Raise Request State Error
            context = error_context_generate('Request Closed', 'Request is Already Closed', '')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        if (request.user.is_benefactor and request.user != benefactor.user) or (
                    request.user.is_charity and request.user != charity.user):
            # TODO Raise Authentication Error
            context = error_context_generate('Access Error', 'You Don\'t Have Permission to Accept This Request', '')
        project = get_object(Project, id=req.nonfinancialproject.project.id)
        if project.type is 'financial':
            # TODO Raise Project Type Error
            context = error_context_generate('Project Type Error', 'Project is Financial', '')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        if project.benefactors.count() > 0 or project.project_state != 'open':
            # TODO Raise Project Occupied Error
            context = error_context_generate('Project Occupied', 'Project is Already Taken by Another Benefactor', '')
            template = loader.get_template('accounts/error_page.html')
            return HttpResponse(template.render(context, request))
        project.benefactors.add(benefactor)
        if len(charity.benefactor_history.filter(user=benefactor.user)) == 0:
            charity.benefactor_history.add(benefactor)
        project.project_state = 'in_progress'
        if request.user.is_benefactor:
            new_notification = Notification.objects.create(type='request_accept', user=charity.user,
                                                           datetime=datetime.datetime.now())
            new_notification.description = 'Your Cooperation Request for Project ' + project + ' Has Been Accepted'
            new_notification.save()
        else:
            new_notification = Notification.objects.create(type='request_accept', user=benefactor.user,
                                                           datetime=datetime.datetime.now())
            new_notification.description = 'Your Cooperation Request for Project ' + project + ' Has Been Accepted'
            new_notification.save()
        req.state = 'closed'
        req.save()
        if request.user.is_charity:
            Logger.accept_request(request.user, benefactor.user, project)
        else:
            Logger.accept_request(request.user, charity.user, project)
        # TODO Success Redirect
        return HttpResponse([])
    except:
        # TODO Raise Unexpected Error
        return HttpResponse([])


@csrf_exempt
def deny_request(request, rid):
    if not request.user.is_authenticated:
        # TODO Raise Authentication Error
        context = sign_in_error()
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    if not request.user.is_active:
        context = error_context_generate('Deactivated Account Error',
                                         'Your Account Has Been Marked as Deactivated!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
    try:
        req = get_object(CooperationRequest, id=rid)
        benefactor = req.benefactor
        charity = req.charity
        if req.state is 'closed':
            # TODO Raise Request State Error
            return HttpResponse([])
        if (request.user.is_benefactor and request.user != benefactor.user) or (
                    request.user.is_charity and request.user != charity.user):
            # TODO Raise Authentication Error
            return HttpResponse([])
        project = get_object(Project, id=req.nonfinancialproject.project.id)
        if project.type is 'financial':
            # TODO Raise Project Type Error
            return HttpResponse([])
        if request.user.is_benefactor:
            new_notification = Notification.objects.create(type='request_deny', user=charity.user,
                                                           datetime=datetime.datetime.now())
            new_notification.description = 'Your Cooperation Request for Project ' + project + ' Has Been Denied'
            new_notification.save()
        else:
            new_notification = Notification.objects.create(type='request_deny', user=benefactor.user,
                                                           datetime=datetime.datetime.now())
            new_notification.description = 'Your Cooperation Request for Project ' + project + ' Has Been Denied'
            new_notification.save()
        req.save()
        if request.user.is_charity:
            Logger.deny_request(request.user, benefactor.user, project)
        else:
            Logger.deny_request(request.user, charity.user, project)
        # TODO Success Redirect
        return HttpResponse([])
    except:
        # TODO Raise Unexpected Error
        context = error_context_generate('Unexpected Error', 'Some Required Files are Lost or Damaged!', '')
        template = loader.get_template('accounts/error_page.html')
        return HttpResponse(template.render(context, request))
