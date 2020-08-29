from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'book/index.html')

def extend(request):
    return render(request,'book/extend.html')

def extend2(request):
    return render(request,'book/extend2.html')