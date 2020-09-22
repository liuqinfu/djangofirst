from django.urls import path, re_path
from app01.views import *

urlpatterns = [
    path('reg/', reg),
    path('func_kks/',func,name='ooo'),
    path('json',json),
    path('upload',upload),
    path('ajax',ajax,name='ajax'),
    path('ajax/send/json',ajaxSendJsonData,name='ajaxSendJsonData'),
    path('ajax/send/file',ajaxSendFileData,name='ajaxSendFileData')
]