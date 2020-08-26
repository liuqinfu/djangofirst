from django.urls import path, re_path,include
from tag import views

urlpatterns = [
    re_path('^$', views.home),
]