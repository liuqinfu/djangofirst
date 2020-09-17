from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from bookmanage import models

def index(request):
    return render(request,'book/index.html')

def extend(request):
    return render(request,'book/extend.html')

def extend2(request):
    return render(request,'book/extend2.html')

def bookList(request):
    books = models.Book.objects.all()
    return render(request,'book/books.html',locals())

def addbook(request):
    publishs = models.Publish.objects.all()
    authors = models.Author.objects.all()
    return render(request,'book/addbook.html',locals())

def saveNewbook(request):
    name = request.POST.get('name')
    price = request.POST.get('price')
    publishTime = request.POST.get('publishTime')
    publish = request.POST.get('publish')
    authors = request.POST.getlist('authors')
    print(name,price,publish,publishTime,authors)
    book = models.Book.objects.create(name=name,price=price,publishTime=publishTime,publish_id=publish)
    models.Book.objects.bulk_create() #批量插入   节省插入时间
    book.authors.set(authors)
    book.save()
    bookListHtml = reverse('book:books')
    return redirect(bookListHtml)

def editbook(request,bookId):
    book = models.Book.objects.filter(pk=bookId).first()
    publishs = models.Publish.objects.all()
    authors = models.Author.objects.all()
    return render(request,'book/editbook.html',locals())

def saveedit(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    price = request.POST.get('price')
    publishTime = request.POST.get('publishTime')
    publish = request.POST.get('publish')
    authors = request.POST.getlist('authors')
    print(name,price,publish,publishTime,authors)
    book = models.Book.objects.filter(pk=id).first()
    book.name = name
    book.price = price
    book.publishTime = publishTime
    book.publish.id = publish
    book.authors.set(authors)
    book.save()
    bookListHtml = reverse('book:books')
    return redirect(bookListHtml)

def deletebook(request,book_id):
    models.Book.objects.filter(pk=book_id).delete()
    bookListHtml = reverse('book:books')
    return redirect(bookListHtml)

def publishList(request):
    publishs = models.Publish.objects.all()
    return render(request,'book/publishs.html',locals())

def authorList(request):
    authors = models.Author.objects.all()
    return render(request,'book/authors.html',locals())