from django.shortcuts import render,HttpResponse,redirect,reverse

# Create your views here.
from app01.models import User


def login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        user = User.objects.filter(uname=uname).first()
        if user:
            if user.password == password:
                return HttpResponse('登录成功')
            else:
                return HttpResponse('密码错误')
        else:
            return HttpResponse('用户名不存在')
    return render(request, 'app01/login.html')


def reg(request):
    print(reverse('app01:ooo'))
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        User.objects.create(uname=uname, password=password)
        return HttpResponse('恭喜，注册成功')
    return render(request, 'app01/reg.html')


def show(request):
    allUser = User.objects.all()
    # return render(request, 'show.html', {'allUser': allUser})
    return render(request, 'app01/show.html', locals())


def edit(request):
    userId = request.GET.get('id')
    edit_obj = User.objects.filter(id=userId).first()
    if request.method == 'POST':
        uname = request.POST.get('uname')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        password = request.POST.get('password')
        # 方式1
        # User.objects.filter(id=userId).update(uname = uname,age=age,sex =sex,password = password)
        # 方式2  当字段多的时候 效率非常低  底层：无论字段是否有更新，都执行更新，即：覆盖
        edit_obj.uname = uname
        edit_obj.age = age
        edit_obj.sex = sex
        edit_obj.password = password
        edit_obj.save()
        return redirect('/show')
    return render(request, 'app01/edit.html', locals())


def delete(request):
    userId = request.GET.get('id')
    User.objects.filter(id=userId).delete()
    return redirect('/show')


def home(request):
    return HttpResponse('home页面')


def pathParam(request, param1, param2):
    print(param1, param2)
    return HttpResponse('无名分组：路径索引参数')


def kwargs(request, year, month):
    print(year, month)
    return HttpResponse('有名分组：关键字参数')


def 反向解析(request):
    # 后端反向解析
    print(reverse('ooo'))
    return render(request, 'app01/反向解析.html')


def func(request):
    return HttpResponse('func')
