from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('create_new', views.CreateProjectForm.as_view, name='create_project_form'),
    path('create_new_project', views.create_new_project, name='create_project_submit'),
    path('non-fin-search', views.find_non_financial_projects_search_results, name='non-fin-search'),
]
