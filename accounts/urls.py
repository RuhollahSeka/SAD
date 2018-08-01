from django.conf.urls import url
from django.urls import path

from . import views, android_views

app_name = 'accounts'

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup_view'),
    path('register/', views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('login_user/', views.login_user, name='login_user'),
    # path('logout_user/', views.logout_user, name='logout_user'),
    path('recover_password/', views.recover_password, name='recover_password'),
    path('recover_password/<int:uid>/<slug:rec_str>/', views.recover_pwd,name='recover_pwd'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('benefactor_dashboard/', views.benefactor_dashboard, name='benefactor_dashboard'),
    path('charity_dashboard/', views.charity_dashboard, name='charity_dashboard'),

    path('customize_user/', views.customize_user_data, name='customize_user_view'),
    path('add_benefactor_credit/', views.add_benefactor_credit, name='add_benefactor_credit'),
    path('customize_user/register/', views.customize_user, name='customize_user'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('error_page/', views.ErrorView.as_view(), name='error_page'),

    path('android-login', android_views.android_login, name='android_login'),
    path('android-signup', android_views.android_signup, name='android_signup')
]


