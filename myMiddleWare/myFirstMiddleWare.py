from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


#自定义中间件

class myFirstMiddleware(MiddlewareMixin):

    def process_request(self,request):
        print('我是第一个自定义的中间件中的process_request方法')
        # return HttpResponse('我是第一个自定义的中间件中的process_request方法返回的')

    def process_response(self,request,response):
        print('我是第一个自定义的中间件中的process_response方法')
        # return response
        return HttpResponse('我是第一个自定义的中间件中的process_response方法返回的')

class mySecondMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print('我是第二个自定义的中间件中的process_request方法')

    def process_response(self,request,response):
        print('我是第二个自定义的中间件中的process_response方法')
        return response