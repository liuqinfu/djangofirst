from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from bookmanage import models

# 装饰器
# 校验用户是否登陆
def check_login(func):
    def check(request, *args, **kwargs):
        uname = request.COOKIES.get('uname')
        if uname:
            res = func(request, *args, *kwargs)
        else:
            # res = login(request,request.get_full_path_info())
            res = redirect('/book?target=%s' % request.get_full_path_info())
        return res
    return check


# csrf_protect装饰的方法需要校验csrf
# csrf_exempt装饰的方法忽略校验csrf

# CBV模式实现url资源控制
# CBV模式加装饰器的方式2 (可以给指定方法,并且可以指定多个方法)
# @method_decorator(check_login,name='get')
# @method_decorator(check_login,name='post')
# @method_decorator(csrf_protect,name='post') 有效
# @method_decorator(csrf_exempt,name='post') 无效
# @method_decorator(csrf_exempt,name='dispatch') 有效
class MyView(View):

    # CBV模式加装饰器的方式3  (原理是CBV底层执行了dispatch方法)
    # @method_decorator(csrf_protect) 有效
    # @method_decorator(csrf_exempt) 有效
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)

    # CBV模式加装饰器的方式1
    # @method_decorator(csrf_protect) 有效
    # @method_decorator(csrf_exempt) 无效
    @method_decorator(check_login)
    def get(self,request):
        return HttpResponse("这是get请求")

    # @method_decorator(csrf_protect) 有效
    # @method_decorator(csrf_exempt) 无效
    def post(self,request):
        return HttpResponse("这是post请求")


def login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        if uname == 'json' and password == '123456':
            target = request.GET.get('target')
            response = redirect(target or 'index/')
            response.set_cookie('uname', uname + password,max_age=1800,expires=1800) #expires针对IE浏览器 超时时间设置为5s   max_age除了IE浏览器之外的超时时间设置为60s
            return response
    return render(request, 'book/login.html')

@check_login
def index(request):
    return render(request, 'book/index.html')


@check_login
def extend(request):
    return render(request, 'book/extend.html')


@check_login
def extend2(request):
    return render(request, 'book/extend2.html')


@check_login
def bookList(request):
    books = models.Book.objects.all()
    deleteUrl = reverse('book:delete')
    return render(request, 'book/books.html', locals())


@check_login
def addbook(request):
    publishs = models.Publish.objects.all()
    authors = models.Author.objects.all()
    return render(request, 'book/addbook.html', locals())


@check_login
def saveNewbook(request):
    name = request.POST.get('name')
    price = request.POST.get('price')
    publishTime = request.POST.get('publishTime')
    publish = request.POST.get('publish')
    authors = request.POST.getlist('authors')
    print(name, price, publish, publishTime, authors)
    book = models.Book.objects.create(name=name, price=price, publishTime=publishTime, publish_id=publish)
    # models.Book.objects.bulk_create()  # 批量插入   节省插入时间
    book.authors.set(authors)
    book.save()
    bookListHtml = reverse('book:books')
    return redirect(bookListHtml)


@check_login
def editbook(request, bookId):
    book = models.Book.objects.filter(pk=bookId).first()
    publishs = models.Publish.objects.all()
    authors = models.Author.objects.all()
    return render(request, 'book/editbook.html', locals())


@check_login
def saveedit(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    price = request.POST.get('price')
    publishTime = request.POST.get('publishTime')
    publish = request.POST.get('publish')
    authors = request.POST.getlist('authors')
    print(name, price, publish, publishTime, authors)
    book = models.Book.objects.filter(pk=id).first()
    book.name = name
    book.price = price
    book.publishTime = publishTime
    book.publish.id = publish
    book.authors.set(authors)
    book.save()
    bookListHtml = reverse('book:books')
    return redirect(bookListHtml)


@check_login
def deletebook(request, book_id):
    models.Book.objects.filter(pk=book_id).delete()
    bookListHtml = reverse('book:books')
    return redirect(bookListHtml)

@check_login
def delete(request):
    bookId = request.POST.get('bookId')
    models.Book.objects.filter(pk = bookId).delete()
    res = {'code': 200, 'msg': 'success', 'data': bookId}
    return JsonResponse(res)


@check_login
def publishList(request):
    publishs = models.Publish.objects.all()
    return render(request, 'book/publishs.html', locals())


@check_login
def authorList(request):
    authors = models.Author.objects.all()
    return render(request, 'book/authors.html', locals())
