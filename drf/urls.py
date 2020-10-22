
from django.contrib import admin
from django.urls import path, re_path,include

import tag.urls as tagurls
import app01.views as app01View

from rest_framework.routers import DefaultRouter
from drf.views import StudentViewSet

router = DefaultRouter() #可以处理视图的路由器
router.register('student',StudentViewSet) #向路由器中注册视图集

urlpatterns = [


]

urlpatterns+=router.urls
