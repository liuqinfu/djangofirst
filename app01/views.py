from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http import JsonResponse
from django import forms
import json
# Create your views here.
from app01.models import User

class MyForm(forms.Form):
    uname = forms.CharField(min_length=3,max_length=8,label='用户名',error_messages={
        'min_length':'最小长度为3',
        'max_length':'最大长度为8',
        'required':'用户名不能为空'
    })
    password = forms.CharField(min_length=3,max_length=8,label='密码',error_messages={
        'min_length':'最小长度为3',
        'max_length':'最大长度为8',
        'required':'密码不能为空'
    })
    confirm = forms.CharField(min_length=3, max_length=8, label='确认密码', error_messages={
        'min_length': '最小长度为3',
        'max_length': '最大长度为8',
        'required': '密码不能为空'
    })
    email = forms.EmailField(min_length=3,max_length=10,label='邮箱',error_messages={
        'min_length':'最小长度为3',
        'max_length':'最大长度为10',
        'required':'邮箱不能为空',
        'invalid':'邮箱无效'
    })

    #钩子函数  钩子函数是在声明校验通过后的第二层自定义校验

    #局部钩子函数只作用在一个字段上面
    def clean_uname(self):
        uname_ = self.cleaned_data['uname']
        if '666' in uname_:
            self.errors['uname']=['光喊666是没有用的']
        return uname_

    #全局钩子函数可以作用在多个字段
    def clean(self):
        password_ = self.cleaned_data['password']
        confirm_ = self.cleaned_data['confirm']
        if not password_ == confirm_:
            self.errors['confirm']=['密码输入不一致']
        return self.cleaned_data


def login(request):
    form_obj = MyForm()
    if request.method == 'POST':
        # uname = request.POST.get('uname')
        # password = request.POST.get('password')
        # email = request.POST.get('email')
        # user = User.objects.filter(uname=uname).first()
        # if user:
        #     if user.password == password:
        #         return HttpResponse('登录成功')
        #     else:
        #         return HttpResponse('密码错误')
        # else:
        #     return HttpResponse('用户名不存在')
        form_obj = MyForm(request.POST)
    return render(request, 'app01/login.html',locals())


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

def json(request):
    dicts ={'name':'李章博',"sex":'男'}
    return JsonResponse(dicts,json_dumps_params = {'ensure_ascii':False})

def upload(request):
    if request.method == 'GET':
        return render(request,'app01/upload.html')
    name = request.POST.get('name')
    file_obj = request.FILES.getlist('file')
    print(file_obj,type(file_obj))
    with open(file_obj.name,'wb') as f:
        for line in file_obj:
            f.write(line)
    return HttpResponse('上传成功')

def ajax(request):
    if request.method == 'POST':
        v1 = request.POST.get('val1')
        v2 = request.POST.get('val2')
        res = int(v1) + int(v2)
        res = {'code':200,'data':res,'msg':'success'}
        return JsonResponse(res)
    else:
        return render(request,'app01/ajax.html')

def ajaxSendJsonData(request):
    if request.is_ajax():
        print(request.POST)
        print(request.body)
        import json
        params = json.loads(request.body)
        print(params)
        return HttpResponse("success")
    return render(request,'app01/ajax_send_jsonData.html')

def ajaxSendFileData(request):
    if request.is_ajax():
        print(request.POST)
        print(request.FILES)
        return HttpResponse("success")
    return render(request,'app01/ajax_send_fileData.html')
