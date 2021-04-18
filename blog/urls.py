"""MinimalBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage, name='Home'),

    path('login/', auth_views.LoginView.as_view(template_name='login_register.html',
                                                redirect_authenticated_user=True), name='Login'),
    path('logout/', auth_views.LogoutView.as_view(), name='Logout'),

    path('register/', views.register, name='Register'),
    path('profile/', views.profile, name='Profile'),

    # # Password Reset Views
    # path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html',
    #                                                              form_class=CustomPasswordResetForm), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='users/password_reset_done.html'), name='password_reset_done'),

    # path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name='users/password_reset_confirm.html', form_class=CustomSetPasswordForm), name='password_reset_confirm'),

    # path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
