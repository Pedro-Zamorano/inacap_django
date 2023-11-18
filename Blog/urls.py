from django.contrib import admin
from django.urls import path
from .views import home_view, register_view, logout_view, login_view, create_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('create/', create_view, name='create'),
]