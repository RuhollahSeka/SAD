from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from projects.models import *
from django.template import loader


# Create your views here.


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

