from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from bbs.forms import RegisterForm
from bbs import models

def index(request):
    return render(request, 'bbs/index.html')




def register(request):
    register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid:
            name_ = request.POST.get('name')
            password_ = request.POST.get('password')
            email_ = request.POST.get('email')
            #插入数据库
            models.User.objects.create_user(username=name_,password=password_,email=email_)
            return HttpResponse('注册成功')
    return render(request,'bbs/register.html',locals())
