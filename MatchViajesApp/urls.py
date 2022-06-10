from django.contrib import admin
from django.urls import path
from MatchViajesApp import views

urlpatterns = [
    path('', views.home, name='Home'),
]