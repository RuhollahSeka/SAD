"""AZED URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views



urlpatterns = [

    path('accounts/', include('accounts.urls')),
    path('projects/', include('projects.urls')),

    path('admin/', views.admin_dashboard, name='admin'),
    path('admin/charity/', views.admin_get_charities, name='admin_charity'),
    path('admin/benefactor/', views.admin_get_benefactors, name='admin_benefactor'),
    path('admin/activate_user/uid=<int:uid>/', views.activate_user, name='admin_activate'),
    path('admin/deactivate_user/uid=<int:uid>/', views.deactivate_user, name='admin_deactivate'),
    path('admin/ability_tags/', views.admin_get_tags, name='admin_tags'),
    path('admin/tx/', views.admin_get_contributions, name='admin_tx'),
    path('admin/add_admin/', views.add_new_admin, name='add_admin'),
    path('admin/add_tag/', views.add_new_admin, name='add_admin'),
    path('admin/add_benefactor/', views.admin_add_benefactor, name='add_benefactor'),
    path('admin/edit_benefactor/uid=<int:uid>/', views.admin_edit_benefactor, name='edit_benefactor'),
    path('admin/add_charity/', views.admin_add_charity, name='add_charity'),

    path('', views.index, name='Home'),
    path('error/',views.ErrorView.as_view(),name='error_page'),
    path('error/red=<slug:redirect_address>/',views.error_redirect,name='error_redirect'),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    #path('accounts/signup/charityf/', views.CharitySignUpView.as_view(), name='charity_signupf'),




]



