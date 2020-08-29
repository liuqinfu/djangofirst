from django.shortcuts import render
import datetime

# Create your views here.

def home(request):
    #模板语法传值
    i = 123
    f = 11.23
    s = '你好'
    bool = False
    set = {'123',456}
    dic = {'name':'张三','age':26,'hobbys':['下棋','王者荣耀','英雄联盟']}
    lis = ['123','qwe',456,'dsa',1114,124343,1321321]

    file_size = 1024*1024 #文件大小
    time = datetime.datetime.now()
    info='第三方酒店房间多少积分分多少九方看了大数据分多少收费的司法鉴定所开房记录SDK是否精吊上课了房间时砥砺奋进老师的'
    words='my name is liuqinfu i`m a man and i`m from china'
    str = 'i love you and you?'
    alert = '<script>alert(123)</script>'
    #后端转义
    h1 = '<h1>你好</h1>'
    from django.utils.safestring import mark_safe
    h1 = mark_safe(h1)
    return render(request,'tag/home.html',locals())
