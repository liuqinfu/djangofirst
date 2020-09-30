from django.contrib import admin
from django.urls import path, re_path

from bbs import views

from django.views.static import serve
from blog import settings

urlpatterns = [
    #暴露后端指定文件夹资源
    re_path('^media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),

    re_path('^$',views.home),
    path('get_code',views.get_code,name = 'get_code'),
    path('login', views.login,name='login'),
    path('register', views.register,name='register'),
    path('home',views.home,name='home'),
    path('logout',views.logout,name='logout'),
    path('changepassword',views.changepassword,name='changepassword'),

]