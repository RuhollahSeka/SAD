from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from projects.models import *
from django.template import loader


# Create your views here.

def find_non_financial_projects_search_results(request):
    project_name = request.POST.get('search_non_financial_project_name')
    charity_name = request.POST.get('search_non_financial_charity_name')
    benefactor_name = request.POST.get('search_non_financial_benefactor_name')
    project_state = request.POST.get('search_non_financial_project_state')
    ability_name = request.POST.get('search_non_financial_ability_name')
    tags = request.POST.get('search_non_financial_tags')
    start_date = request.POST.get('search_non_financial_start_date')
    end_date = request.POST.get('search_non_financial_end_date')
    weekly_schedule = create_query_schedule(request.POST.get('search_non_financial_schedule'))
    schedule = [start_date, end_date, weekly_schedule]
    min_required_hours = request.POST.get('searchnon_financial_min_required_hours')
    min_date_overlap = request.POST.get('search_non_financial_min_date_overlap')
    min_time_overlap = request.POST.get('search_non_financial_min_time_overlap')
    age = request.POST.get('search_non_financial_age')
    gender = request.POST.get('search_non_financial_gender')
    country = request.POST.get('search_non_financial_country')
    province = request.POST.get('search_non_financial_province')
    city = request.POST.get('search_non_financial_city')
    project_queryset = search_non_financial_project(project_name, charity_name, benefactor_name, project_state,
                                                    ability_name, tags, schedule, min_required_hours, min_date_overlap,
                                                    min_time_overlap, age, gender, country, province, city)
    return render(request, 'url', {'result_non_financial_projects': list(project_queryset)})


def find_financial_project_search_results(request):
    project_name = request.POST.get('search_financial_project_name')
    charity_name = request.POST.get('search_financial_charity_name')
    benefactor_name = request.POST.get('search_financial_benefactor_name')
    project_state = request.POST.get('search_financial_project_state')
    min_progress = request.POST.get('search_financial_min_progress')
    max_progress = request.POST.get('search_financial_max_progress')
    min_deadline_date = request.POST.get('search_financial_min_deadline_date')
    max_deadline_date = request.POST.get('search_financial_max_deadline_date')
    project_queryset = search_financial_project(project_name, charity_name, benefactor_name, project_state,
                                                min_progress, max_progress, min_deadline_date, max_deadline_date)
    return render(request, 'url', {'result_financial_projects': list(project_queryset)})


def find_charity_search_results(request):
    charity_name = request.POST.get('search_charity_name')
    min_score = request.POST.get('search_charity_min_score')
    max_score = request.POST.get('search_charity_max_score')
    min_related_projects = request.POST.get('search_charity_min_related_projects')
    max_related_projects = request.POST.get('search_charity_max_related_projects')
    min_finished_projects = request.POST.get('search_charity_min_finished_projects')
    max_finished_projects = request.POST.get('search_charity_max_finished_projects')
    benefactor_name = request.POST.get('search_charity_benefactor_name')
    country = request.POST.get('search_charity_country')
    province = request.POST.get('search_charity_province')
    city = request.POST.get('search_charity_city')
    charity_queryset = search_charity(charity_name, min_score, max_score, min_related_projects, max_related_projects,
                                      min_finished_projects, max_finished_projects, benefactor_name, country, province,
                                      city)
    return render(request, 'url', {'result_charities': list(charity_queryset)})


# TODO handle security and stuff like that
# TODO send more data like scores, overlapped days and overlapped weekly hours
def find_benefactor_search_results(request):
    start_date = request.POST.get('search_benefactor_start_date')
    end_date = request.POST.get('search_benefactor_end_date')
    weekly_schedule = create_query_schedule(request.POST.get('search_benefactor_schedule'))
    schedule = [start_date, end_date, weekly_schedule]
    min_required_hours = request.POST.get('search_benefactor_min_required_hours')
    min_date_overlap = request.POST.get('search_benefactors_min_date_overlap')
    min_time_overlap = request.POST.get('search_benefactors_min_time_overlap')
    tags = request.POST.get('search_benefactor_tags')
    ability_name = request.POST.get('search_benefactor_ability_name')
    ability_min_score = request.POST.get('search_benefactor_ability_min_score')
    ability_max_score = request.POST.get('search_benefactor_ability_max_score')
    country = request.POST.get('search_benefactor_country')
    province = request.POST.get('search_benefactor_province')
    city = request.POST.get('search_benefactor_city')
    user_min_score = request.POST.get('search_benefactor_user_min_score')
    user_max_score = request.POST.get('search_benefactor_user_max_score')
    gender = request.POST.get('search_benefactor_gender')
    first_name = request.POST.get('search_benefactor_first_name')
    last_name = request.POST.get('search_benefactor_last_name')
    benefactor_queryset = search_benefactor(schedule, min_required_hours, min_date_overlap, min_time_overlap, tags,
                                            ability_name, ability_min_score, ability_max_score, country, province,
                                            city, user_min_score, user_max_score, gender, first_name, last_name)
    benefactor_list = list(benefactor_queryset)
    result_benefactor_data = []
    for benefactor, overlap_data in zip(benefactor_list, search_overlap_data):
        result_benefactor_data.append([benefactor, overlap_data[0], overlap_data[1]])

    return render(request, 'wtf?', {'result_benefactors': result_benefactor_data})


def create_new_project(request):
    if request.user.is_authenticated():
        project = Project.objects.create()
        project.project_name = request.POST['project_name']
        project.charity = request.user
        project.description = request.POST['description']
        project.state = 'open'
        if request.POST['start_date'] is not None:
            project.start_date = datetime.datetime.strptime(request.POST['start_date'], '%y-%m-%d')
        else:
            project.start_date = datetime.date.today()
        project.deadline = datetime.datetime.strptime(request.POST['deadline'], '%y-%m-%d')
        project.save()
        if request.POST['type'] is 'financial':
            project.type = 'financial'
            financial_project = FinancialProject.objects.create()
            financial_project.project = project
            financial_project.target_money = int(request.POST['target_money'])
            financial_project.current_money = 0
            financial_project.save()
        else:
            project.type = 'non-financial'
            non_financial_project = NonFinancialProject.objects.create()
            non_financial_project.project = project
            non_financial_project.save()
        # TODO Fix redirect path
        return HttpResponseRedirect('path')
    else:
        # TODO Fix content
        return HttpResponse(content=[])


def edit_project(request, pk):
    # TODO fix path
    template = loader.get_template('path-to-template')
    if not request.user.is_authenticated():
        return HttpResponse(template.render({'pk': pk, 'error_message': 'Authentication Error!'}, request))
    if not request.method is 'POST':
        return HttpResponse(template.render({'pk': pk, 'error_message': 'Method is not POST!'}, request))
    project = get_object_or_404(Project, pk=pk)
    try:
        dic = request.POST
        project.project_name = dic['project_name']
        project.project_state = dic['project_state']
        project.description = dic['description']
        project.start_date = dic['start_date']
        project.deadline = dic['deadline']
        if project.type is 'financial':
            fin_project = get_object_or_404(FinancialProject, project=project)
            fin_project.target_money = dic['target_money']
            # FIXME should the current_money be editable or not?
            fin_project.current_money = dic['current_money']
            fin_project.save()
        project.save()
    except:
        context = {
            'pk': pk,
            'error_message': 'Error in finding the Project!'
        }
        return HttpResponse(template.render(context, request))
    # FIXME maybe all responses should be Redirects / parameters need fixing
    return HttpResponseRedirect([])


def show_project_data(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # TODO fix template path
    template = loader.get_template('projects/get_project_data_for_edit.html')
    try:
        context = {
            'pk': pk,
            'project_name': project.project_name,
            'description': project.description,
            'project_state': project.project_state,
            'start_date': project.start_date,
            'deadline': project.deadline,
            'type': project.type,
        }
        if project.type is 'financial':
            fin_project = get_object_or_404(FinancialProject, project=project)
            context.update({
                'target_money': fin_project.target_money,
                'current_money': fin_project.current_money
            })
    except:
        context = {
            'pk': pk,
            'error_message': 'Error in finding the Project!'
        }
    return HttpResponse(template.render(context, request))


def add_requirement(request, project_id):
    # FIXME maybe it shouldn't be pk
    project = get_object_or_404(Project, pk=project_id)
    requirement = Requirement.objects.create()
