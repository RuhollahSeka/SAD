from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('projects/create_new', views.CreateProjectForm.as_view, name='create_project_form'),
    path('projects/create_new/submit', views.create_new_project, name='create_project_submit'),
]