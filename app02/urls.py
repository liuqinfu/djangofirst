from django.urls import path, re_path

from app02.views import *

urlpatterns = [
    path('reg/', reg),
    path('func_kks/',func,name='ooo')
]