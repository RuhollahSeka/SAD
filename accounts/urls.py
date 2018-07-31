from django.urls import path

from . import views
from . import android_views

urlpatterns = [
    path('accounts/signup', views.SignUpView.as_view(), name='signup_view'),
    path('accounts/signup/register/', views.signup, name='signup'),

    path('accounts/login/', views.LoginView.as_view(), name='login_view'),
    path('accounts/login/register/', views.login_user, name='login_user'),

    path('accounts/customize_user/', views.customize_user_data, name='customize_user_view'),
    path('accounts/customize_user/register/', views.customize_user, name='customize_user'),

    path('android-all-users', android_views.android_user_list, name='android_all_users')
]


