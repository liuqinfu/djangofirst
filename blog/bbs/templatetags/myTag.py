from django import template
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from bbs import models

register = template.Library()


# inclusion_tag 原理：
# 先定义一个方法
# 在页面上调用它，并且可以传值
# 该方法会生成一些数据并传入到一个html页面中
# 之后将渲染好的页面放到调用该方法的位置
@register.inclusion_tag(name='sidecontent', filename='tag/sidecontent.html')
def myInclusionTag(username):
    # 判断用户是否存在
    user = models.User.objects.filter(username=username).first()
    # 查询分类及对应文章数
    categories = models.Category.objects.filter(site=user.site).annotate(count_num=Count('article__pk')).values('pk',
                                                                                                                'name',
                                                                                                                'count_num')
    labels = models.Label.objects.filter(site=user.site).annotate(count_num=Count('article__pk')).values('pk', 'name',
                                                                                                         'count_num')
    months = models.Article.objects.filter(site=user.site).annotate(month=TruncMonth('create_time')).values(
        'month').annotate(count_num=Count('pk')).values('month', 'count_num')
    return locals()  # list传递给ul.html
