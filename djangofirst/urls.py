"""djangofirst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app01.views import *

urlpatterns = [
    re_path('^$', home),
    path('admin/', admin.site.urls),
    path('login/', login),
    path('reg/', reg),
    # 无名分组
    # re_path('show/(\d+)/(\d+)$', pathParam),
    # 有名分组
    re_path('show/(?P<year>\d+)/(?P<month>\d+)$',kwargs),
    path('show/', show),
    path('edit/', edit),
    path('delete/', delete),
    path('反向解析',反向解析),
    path('func_kks/',func,name='ooo')
]
