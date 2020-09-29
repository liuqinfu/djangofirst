from django.contrib import admin
from django.urls import path, re_path

from bbs import views

urlpatterns = [
    path('get_code',views.get_code,name = 'get_code'),
    path('login', views.login,name='login'),
    path('register', views.register,name='register'),
    path('home',views.home,name='home'),
    path('logout',views.logout,name='logout'),

]