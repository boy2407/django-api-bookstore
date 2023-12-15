from django.contrib import admin
from django.urls import path, include
from . import  views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('register/', views.registration, name='register'),
    path('profile/', views.get_profile, name='profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Email verification URL's
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),
    path('email-verification-sent/', views.email_verification_sent, name='email-verification-sent'),
    path('email-verification-success/', views.email_verification_success, name='email-verification-success'),
    path('email-verification-failed/', views.email_verification_failed, name='email-verification-failed'),
    path('email-verification-failed/', views.email_verification_failed, name='email-verification-failed'),



    # 1 ) Submit our email form
    path('reset-password', auth_views.PasswordResetView.as_view(template_name="user/password/password-reset.html"),
         name='reset_password'),
    # 2) Success message stating that a password reset email was sent
    path('reset-password-sent',
         auth_views.PasswordResetDoneView.as_view(template_name="user/password/password-reset-sent.html"),
         name='password_reset_done'),
    # 3) Password reset link
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="user/password/password-reset-form.html"),
         name='password_reset_confirm'),
    # 4) Success message stating that our password was reset
    path('password-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(template_name="user/password/password-reset-complete.html"),
         name='password_reset_complete'),
]
