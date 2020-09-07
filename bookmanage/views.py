from django.shortcuts import render

# Create your views here.
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

def publishList(request):
    publishs = models.Publish.objects.all()
    return render(request,'book/publishs.html',locals())

def authorList(request):
    authors = models.Author.objects.all()
    return render(request,'book/authors.html',locals())