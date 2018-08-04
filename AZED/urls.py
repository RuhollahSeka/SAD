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

    path('admin/activate_user/uid=<int:uid>/', views.activate_user, name='activate_user'),
    path('admin/deactivate_user/uid=<int:uid>/', views.deactivate_user, name='deactivate_user'),
    path('admin/delete_user/uid=<int:uid>', views.admin_delete_user, name='delete_user'),

    path('admin/ability_tags/', views.admin_get_tags, name='admin_tags'),
    path('admin/tx/', views.admin_get_contributions, name='admin_tx'),
    path('admin/score/', views.admin_get_scores, name='admin_score'),
    path('admin/comment/', views.admin_get_comments, name='admin_comment'),

    path('admin/delete_benefactor_score/score_id=<int:score_id>/', views.admin_delete_benefactor_score, name='delete_benefactor_score'),
    path('admin/delete_charity_score/score_id=<int:score_id>/', views.admin_delete_charity_score, name='delete_charity_score'),
    path('admin/edit_ben_score/score_id=<int:score_id>/', views.admin_edit_benefactor_score, name='edit_benefactor_score'),
    path('admin/edit_char_score/score_id=<int:score_id>/', views.admin_edit_charity_score, name='edit_charity_score'),
    path('admin/add_benefactor_score/', views.admin_add_benefactor_score, name='add_benefactor_score'),
    path('admin/add_charity_score/', views.admin_add_charity_score, name='add_charity_score'),

    path('admin/delete_benefactor_comment/comment_id=<int:comment_id>/', views.admin_delete_benefactor_comment, name='delete_benefactor_comment'),
    path('admin/delete_charity_comment/comment_id=<int:comment_id>/', views.admin_delete_charity_comment, name='delete_charity_comment'),
    path('admin/edit_ben_comment/comment_id=<int:comment_id>/', views.admin_edit_benefactor_comment, name='edit_benefactor_comment'),
    path('admin/edit_char_comment/comment_id=<int:comment_id>/', views.admin_edit_charity_comment, name='edit_charity_comment'),
    path('admin/add_benefactor_comment/', views.admin_add_benefactor_comment, name='add_benefactor_comment'),
    path('admin/add_charity_comment/', views.admin_add_charity_comment, name='add_charity_comment'),

    path('admin/add_admin/', views.add_new_admin, name='add_admin'),

    path('admin/add_tag/', views.admin_add_ability_tag, name='add_tag'),
    path('admin/edit_tag/tag_id=<int:tag_id>/', views.admin_edit_ability_tag, name='edit_tag'),
    path('admin/delete_tag/tag_id=<int:tag_id>/', views.admin_delete_ability_tag, name='delete_tag'),

    path('admin/add_benefactor/', views.admin_add_benefactor, name='add_benefactor'),
    path('admin/edit_benefactor/uid=<int:uid>/', views.admin_edit_benefactor, name='edit_benefactor'),
    path('admin/add_charity/', views.admin_add_charity, name='add_charity'),
    path('admin/edit_charity/uid=<int:uid>/', views.admin_edit_benefactor, name='edit_benefactor'),


    path('', views.index, name='Home'),
    path('error/',views.ErrorView.as_view(),name='error_page'),
    path('error/red=<slug:redirect_address>/',views.error_redirect,name='error_redirect'),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    #path('accounts/signup/charityf/', views.CharitySignUpView.as_view(), name='charity_signupf'),




]

