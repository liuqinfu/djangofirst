from django.urls import path, re_path,include
from bookmanage.views import *

urlpatterns = [
    re_path('^$', index),
    path('extend/',extend,name='extend'),
    path('extend2/',extend2,name='extend2'),

]