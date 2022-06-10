from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='Register'),
    path('login/', views.loginPage, name='Login'),
    path('logout/', views.logoutUser, name='Logout'),
]   