from django.shortcuts import render

# Create your views here.

def home(request):
    #模板语法传值
    i = 123
    f = 11.23
    s = '你好'
    set = {'123',456}
    dic = {'name':'张三','age':26}
    lis = ['123','qwe',456]
    return render(request,'tag/home.html',locals())
