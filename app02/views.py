from django.shortcuts import render,reverse,HttpResponse

# Create your views here.

def reg(request):
    print(reverse('app02:ooo'))
    return HttpResponse('app02:reg')

def func(request):
    return HttpResponse('app02:func')