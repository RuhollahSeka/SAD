from django.conf.urls import url
from django.urls import path

from . import views, android_views

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup_view'),
    path('register/', views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('login_user/', views.login_user, name='login_user'),

    path('customize_user/', views.customize_user_data, name='customize_user_view'),
    path('add_benefactor_credit/', views.add_benefactor_credit, name='add_benefactor_credit'),
    path('customize_user/register/', views.customize_user, name='customize_user'),
    path('user_profile/', views.user_profile, name='user_profile'),


    path('android-login', android_views.android_login, name='android_login'),
    path('android-signup', android_views.android_signup, name='android_signup')
]


