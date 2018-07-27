from django.urls import path

from . import views

urlpatterns = [
    path('signup_view/', views.SignUpView.as_view(), name='signup_view'),
    path('signup/', views.signup, name='signup'),

    path('login_view/', views.LoginView.as_view(), name='login_view'),
    path('login/', views.login_user, name='login_user'),

    path('customize_user_view/', views.CustomizeUserView.as_view(), name='customize_user_view'),
    path('customize_user/', views.customize_user, name='customize_user'),
]


