from django import template

register = template.Library()

#自定义过滤器（参数最多有两个）
@register.filter(name='baby')
def mySum(v1,v2):
    return v1+v2


#自定义标签(参数可以有多个）
@register.simple_tag(name='plus')
def myPlus(a,b,c,d):
    return '%s-%s-%s-%s' % (a,b,c,d)


#inclusion_tag 原理：
# 先定义一个方法
# 在页面上调用它，并且可以传值
# 该方法会生成一些数据并传入到一个html页面中
# 之后将渲染好的页面放到调用该方法的位置
@register.inclusion_tag(name='myul',filename='tag/ul.html')
def myInclusionTag():
    list = [1,2,3,4]
    return locals() #list传递给ul.html