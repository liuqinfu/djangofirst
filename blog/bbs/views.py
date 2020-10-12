from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, F
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from bbs.forms import RegisterForm
from bbs import models

# 图片相关模块 pip3 install pillow
from PIL import Image, ImageDraw, ImageFont

'''
Image:生成图片
ImageDraw：在图片上乱涂乱画
ImageFont：控制字体样式
'''

from io import BytesIO, StringIO

'''
内存管理器模块
BytesIO：临时存储数据，返回的时候数据是二进制数据
StringIO：临时存储数据，返回的时候数据是字符串
'''

# 获取验证码
import random


# 生成随机验证码背景色
def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_code(request):
    # 方式1  直接获取后端线程的图片二进制数据发送给前端
    # with open('avatar/捕获.PNG','rb') as f:
    #     data = f.read()

    # 方式2  利用pillow模块动态产生图片
    # image_obj = Image.new('RGB', (300, 35), 'gray')
    # #将图片对象保存  然后读取出来
    # with open('xxx.png','wb') as f:
    #     image_obj.save(f,'png')
    # with open('xxx.png','rb') as f:
    #     data = f.read()

    # 方式3  方式2的文件存储繁琐 io操作频繁，效率低，借助内存管理模块
    image_obj = Image.new('RGB', (300, 35), get_random())
    io_obj = BytesIO()  # 生成内存管理器对象   可以看成文件句柄
    image_obj.save(io_obj, 'png')

    # 写图片验证码
    # image_obj = Image.new('RGB', (300, 35), get_random())
    image_obj = Image.new('RGB', (300, 35), 'white')
    draw_obj = ImageDraw.Draw(image_obj)
    font_obj = ImageFont.truetype('static/fonts/1.ttf', 30)

    # 生成5位数随机数
    code = ''
    for i in range(5):
        random_super = chr(random.randint(65, 90))  # 根据ascii表将数字转成大写字母
        random_lower = chr(random.randint(97, 122))
        random_int = str(random.randint(0, 9))
        # 从上面三个钟随机选择一个
        tmp = random.choice([random_super, random_lower, random_int])
        # 将验证码写到图片上
        # 一个一个写  可以控制间隙
        draw_obj.text((i * 45, 0), tmp, get_random(), font_obj)
        code += tmp
    # 随机验证码需要在登陆视图函数中使用，做比对
    request.session['code'] = code
    io_obj = BytesIO()
    image_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


def login(request):
    if request.method == 'POST':
        res = {'code': 200, 'msg': 'success'}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if request.session.get('code').upper() == code.upper():
            authenticate = auth.authenticate(request, username=username, password=password)
            if authenticate:
                auth.login(request, authenticate)
                res['url'] = reverse('bbs:home')
            else:
                res['code'] = 201
                res['msg'] = '用户名或密码错误'
        else:
            res['code'] = 202
            res['msg'] = '验证码错误'
        return JsonResponse(res)
    return render(request, 'bbs/login.html')


# 用户注册
def register(request):
    register_form = RegisterForm()
    if request.method == 'POST':
        res = {'code': 200, 'msg': 'success'}
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            cleaned_data = register_form.cleaned_data
            cleaned_data.pop('confirm')
            avatar = request.FILES.get('avatar')
            if avatar:
                cleaned_data['avatar'] = avatar
            # 插入数据库
            models.User.objects.create_user(**cleaned_data)
            res['url'] = reverse('bbs:login')
        else:
            res['code'] = 402
            res['msg'] = 'fail'
            res['errors'] = register_form.errors
        return JsonResponse(res)
    return render(request, 'bbs/register.html', locals())


# 首页
from utils import pagehelper


def home(request):
    article_list = models.Article.objects.all()
    current_page = request.GET.get("page", 1)
    all_count = article_list.count()
    page_obj = pagehelper.Pagination(current_page=current_page, all_count=all_count, per_page_num=10)
    page_queryset = article_list[page_obj.start:page_obj.end]
    return render(request, 'bbs/home.html', locals())


# 登出
@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('bbs:home'), locals())


# 修改密码
@login_required
def changepassword(request):
    if request.is_ajax() and request.method == 'POST':
        res = {'code': 200, 'msg': 'success'}
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        confirmnewpassword = request.POST.get('confirmnewpassword')
        is_right = request.user.check_password(oldpassword)
        if is_right:
            if newpassword == confirmnewpassword:
                if len(newpassword) == 0:
                    res['code'] = 203
                    res['msg'] = '新密码不能为空'
                else:
                    request.user.set_password(newpassword)
                    request.user.save()
            else:
                res['code'] = 202
                res['msg'] = '确认密码与新密码不一致'
        else:
            res['code'] = 201
            res['msg'] = '原密码错误'
        return JsonResponse(res)
    return render(request, 'bbs/home.html', locals())


# 用户站点首页
def usersite(request, username, **kwargs):
    '''
    :param request:
    :param username:
    :param kwargs: 有值，则需要对article_list做进一步筛选
    :return:
    '''
    # 判断用户是否存在
    user = models.User.objects.filter(username=username).first()
    if not user:
        # 返回404页面
        return render(request, 'bbs/404.html')
    # 查询文章
    article_list = models.Article.objects.filter(site__user__username=username)
    if kwargs:
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if condition == 'label':
            article_list = article_list.filter(labels__in=[param])
        elif condition == 'category':
            article_list = article_list.filter(category__pk=param)
        elif condition == 'archive':
            year, month = param.split('-')
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

    current_page = request.GET.get("page", 1)
    all_count = article_list.count()
    page_obj = pagehelper.Pagination(current_page=current_page, all_count=all_count, per_page_num=10)
    page_queryset = article_list[page_obj.start:page_obj.end]
    return render(request, 'bbs/site.html', locals())


# 文章详情
def articledetail(request, username, articleid):
    '''
    文章详情
    :param request:
    :param username: 文章发表用户
    :param artile: 文章唯一编号
    :return:
    '''
    user = models.User.objects.filter(username=username).first()
    article = models.Article.objects.filter(pk=articleid, site__user__username=username).first()
    comments = models.Comment.objects.filter(article=article).all()
    return render(request, 'bbs/article_detail.html', locals())


# 文章点赞点踩
import json


def up_down(request):
    '''
    1、必须为登录用户
    2、不能点赞自己的文章
    3、点赞点踩二选一,且不能重复操作
    :param request:
    :return:
    '''
    res = {'code': 200, 'msg': 'success'}
    is_authenticated = request.user.is_authenticated
    if not is_authenticated:
        login_url = reverse('bbs:login')
        res['code'] = 403
        res['msg'] = '请先<a href="' + login_url + '">登录</a>'
    else:
        articleId = request.POST.get('artileId')
        article = models.Article.objects.filter(pk=articleId).first()
        if article.site.user == request.user:
            res['code'] = 201
            res['msg'] = '不能点赞点踩自己的文档'
        else:
            actions = models.Updown.objects.filter(user=request.user, article=article).all()
            if actions:
                res['code'] = 202
                res['msg'] = '您已经操作过这片文章了'
            else:
                is_up = request.POST.get('is_up')
                is_up = json.loads(is_up)
                with transaction.atomic():
                    models.Updown.objects.create(user=request.user, article=article, is_up=is_up)
                    if is_up:
                        models.Article.objects.filter(pk=articleId).update(up_num=F('up_num') + 1)
                    else:
                        models.Article.objects.filter(pk=articleId).update(down_num=F('down_num') + 1)
    return JsonResponse(res)


# 添加评论
def comment(request):
    if request.is_ajax() and request.method == 'POST':
        res = {'code': 200, 'msg': 'success'}
        if request.user.is_authenticated:
            articleId = request.POST.get('articleId')
            comment = request.POST.get('comment')
            parentId = request.POST.get('parentId')
            soup = BeautifulSoup(comment, 'html.parser')
            tags = soup.findAll()
            for tag in tags:
                if tag.name == 'script':
                    tag.decompose()
            comment=str(soup)
            # 评论表  评论数
            with transaction.atomic():
                models.Comment.objects.create(user=request.user, article_id=articleId, content=comment,
                                              parent_id=parentId)
                models.Article.objects.filter(pk=articleId).update(comment_num=F('comment_num') + 1)
            res['comment']=comment
        else:
            res['code']: 403
            res['msg']: '请先登录'
        return JsonResponse(res)


@login_required
def backend(request):
    article_list = models.Article.objects.filter(site__user=request.user)
    current_page = request.GET.get("page", 1)
    all_count = article_list.count()
    page_obj = pagehelper.Pagination(current_page=current_page, all_count=all_count, per_page_num=10)
    page_queryset = article_list[page_obj.start:page_obj.end]
    return render(request, 'bbs/backend/article_manage.html', locals())


from bs4 import BeautifulSoup
@login_required
def addarticle(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        labels = request.POST.getlist('label')
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.findAll()
        for tag in tags:
            if tag.name == 'script':
                tag.decompose()
        desc = soup.text[0:100]
        content=str(soup)

        with transaction.atomic():
            article_obj = models.Article.objects.create(title=title, content=content, desc=desc, category_id=category_id,
                                                   site=request.user.site)
            label_obj_list=[]
            for label_id in labels:
                label_obj = models.Article2Label(article=article_obj, label_id=label_id)
                label_obj_list.append(label_obj)
            models.Article2Label.objects.bulk_create(label_obj_list)
        return redirect(to=reverse('bbs:backend'))

    category_list = models.Category.objects.filter(site__user=request.user).all()
    label_list = models.Label.objects.filter(site__user=request.user).all()
    return render(request, 'bbs/backend/article_add.html', locals())
