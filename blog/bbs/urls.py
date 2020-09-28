from django.contrib import admin
from django.urls import path, re_path

from bbs import views

urlpatterns = [
    re_path('^$', views.index),
    path('register', views.register),

]