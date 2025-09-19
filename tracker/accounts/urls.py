from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('otp_verification/',views.otp_verification,name='otp_verification')
]
