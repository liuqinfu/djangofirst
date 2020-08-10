from django.urls import path, re_path
from app01.views import *

urlpatterns = [
    re_path('^$', home),
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