from django.contrib import admin
from django.urls import path, re_path

from bbs import views

from django.views.static import serve
from blog import settings

urlpatterns = [
    # 暴露后端指定文件夹资源
    re_path('^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    path('backend',views.backend,name='backend'),
    path('backend/addarticle',views.addarticle,name='addarticle'),
    # 首页
    re_path('^$', views.home, name='home'),
    # 获取验证码
    path('get_code', views.get_code, name='get_code'),
    # 登陆
    path('login', views.login, name='login'),
    # 注册
    path('register', views.register, name='register'),
    # 登出
    path('logout', views.logout, name='logout'),
    # 修改密码
    path('changepassword', views.changepassword, name='changepassword'),
    # 点赞点踩
    path('up_down',views.up_down,name='up_down'),
    # 评论
    path('comment',views.comment,name='comment'),
    # 站点首页
    re_path('^(?P<username>\w+)/$', views.usersite, name='usersite'),
    ###侧边栏筛选功能
    # # 站点首页（文章按标签过滤）
    # re_path('(?P<username>\w+)/label/(?P<label>\d+)',views.usersite,name='usersitebylabel'),
    # # 站点首页（文章按类别过滤）
    # re_path('(?P<username>\w+)/category/(?P<category>\d+)',views.usersite,name='usersitebycategory'),
    # # 站点首页（文章按日期过滤）
    # re_path('(?P<username>\w+)/archive/(?P<month>\w+)',views.usersite,name='usersitebymonth'),
    # 站点综合
    re_path('^(?P<username>\w+)/(?P<condition>label|category|archive)/(?P<param>.*)/', views.usersite,name='sitebycondition'),
    # 文章详情
    re_path('^(?P<username>\w+)/article/(?P<articleid>\d+)/',views.articledetail,name='articledetail'),

]
