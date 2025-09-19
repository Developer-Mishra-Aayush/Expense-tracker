from django.contrib import admin
from django.urls import path
from . import views

app_name = 'calculate'

urlpatterns = [
    path('',views.index,name='index'),
    path('delete-transactions/<uuid>/',views.delete_transactions,name='delete_transactions'),
    path('delete_all_transactions/',views.delete_all_transactions,name='delete_all_transactions'),
]
