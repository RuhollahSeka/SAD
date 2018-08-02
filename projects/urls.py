from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('create_new', views.CreateProjectForm.as_view(), name='create_project_form'),
    path('create_new_project', views.create_new_project, name='create_project_submit'),
    path('non-fin-search', views.find_non_financial_projects_search_results, name='non-fin-search'),
    path('non-fin-advanced-search', views.find_non_financial_projects_advanced_search_results,
         name='non-fin-advanced-search'),
    url(r'^non-fin-project/(?P<pk>[a-zA-Z0-9]+)/$', views.show_project_data, name='non-fin-project'),
]

# i fucking hate my fucking life and this fucking situation, god damn this fucking shit, fuck me...
