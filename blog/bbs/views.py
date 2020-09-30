from django.contrib import auth
from django.contrib.auth.decorators import login_required
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
                res['url'] = '/bbs/home'
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


from utils import pagehelper
def home(request):
    article_list = models.Article.objects.all()
    current_page = request.GET.get("page", 1)
    all_count = article_list.count()
    page_obj = pagehelper.Pagination(current_page=current_page, all_count=all_count, per_page_num=10)
    page_queryset = article_list[page_obj.start:page_obj.end]
    return render(request, 'bbs/home.html', locals())


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('bbs:home'), locals())

@login_required
def changepassword(request):
    if request.is_ajax() and request.method == 'POST':
        res={'code':200,'msg': 'success'}
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
                res['code']=202
                res['msg']='确认密码与新密码不一致'
        else:
            res['code']=201
            res['msg'] = '原密码错误'
        return JsonResponse(res)
    return render(request, 'bbs/home.html', locals())
