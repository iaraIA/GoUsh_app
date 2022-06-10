from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('cargarViaje/', views.cargarViaje, name='CargarViaje'),
    path('verViaje/', views.verViaje, name='VerViaje'),
    path('misViajes/', views.misViajes , name='misViajes'),
]   
    