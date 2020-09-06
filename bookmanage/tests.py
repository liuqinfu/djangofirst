from datetime import datetime

from django.db.models import Avg, Max, Min, Sum, Count, Value, Q
from django.db.models.functions import Concat
from django.test import TestCase

# Create your tests here.
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangofirst.settings')
    import django
    django.setup()
    # 可以写测试代码了
    from bookmanage import models
    '''
    单表操作
    '''
    # objects_all = models.Book.objects.all()
    # print(objects_all.first().name)
    # #增
    # create = models.Publish.objects.create(name='曹雪芹', addr='宋')
    # print(create.name)
    # #删
    # delete = models.Publish.objects.filter(pk=3).delete()
    # print(delete)
    # 修改
    # update = models.Publish.objects.filter(pk=4).update(addr='宋朝')

    # objects_filter = models.Publish.objects.filter(addr='宋朝')
    # first = objects_filter.first()
    # first.addr = '宋朝'
    # update = first.save()

    #     神奇的双下划线
    # 1 价格大于120的书
    # first = models.Book.objects.filter(price__gt=120)
    # print(first.first())

    # 2 价格大于等于120.3
    # objects_filter = models.Book.objects.filter(price__gte=120.3)
    # print(objects_filter.first())

    # 3 价格为120.3 或 130 或 150
    # objects_filter = models.Book.objects.filter(price__in=[120.3, 130, 150])
    # print(objects_filter)

    # 4 价格在120到150之间  顾头顾尾
    # objects_filter = models.Book.objects.filter(price__range=[120, 150])
    # print(objects_filter)

    # 5 查询名字中含有"演"的 默认区分大小写
    # objects_filter = models.Book.objects.filter(name__contains='演')
    # 忽略大小写
    # objects_filter = models.Book.objects.filter(name__icontains='演')
    # print(objects_filter)

    # 6 以"三"开头
    # objects_filter = models.Book.objects.filter(name__startswith='三')
    # 以"演义"结尾
    # objects_filter = models.Book.objects.filter(name__endswith='演义')
    # print(objects_filter)

    # 7 9月份发布的书
    # objects_filter = models.Book.objects.filter(publishTime__month='9')
    # print(objects_filter)

    '''
    多表操作
    '''
    # 一对多 增删改查
    #增  创建一本书
    # 1 直接写实际字段
    # models.Book.objects.create(name='王二小',price=98,publish_id=1)
    # 2  放虚拟对象
    # publish = models.Publish.objects.filter(pk=4).first()
    # models.Book.objects.create(name='刘金元', price=50, publish=publish)

    # 删
    # models.Publish.objects.filter(pk=5).delete() #级联删除

    # 修改
    # models.Book.objects.filter(name='刘金元').update(publish_id=1)

    # 多对多 增删改查  就是操作第三张表
    # 1 给书籍添加作者
    # author1 = models.Author.objects.filter(pk=1).first()
    # author3 = models.Author.objects.filter(pk=3).first()
    # book = models.Book.objects.filter(pk=5).first()
    # print(book.authors)#这里已经到了第三张表了

    # book.authors.add(author1)
    # book.authors.add(author3)
    # book.authors.add(author1,author3) # book.authors.add(1,3)
    # 2 删除书籍的一个作者
    # book.authors.remove(author1,3)
    # 3 修改书籍 作者关系
    # book.authors.set([1,2]) #book.authors.add(author1,author2)
    # 4 清空书籍与作者的关系
    # book.authors.clear()

    """
    多表查询存在正反向问题
    外键字段在A表中，从通过A获取B 称为正向查询，反之 称为反向查询
    正向查询用字段  反向查询用表名小写
    """
    #### 基于子查询的正向查询
    # 查询书籍主键为1的出版社名称
    # book = models.Book.objects.filter(pk=1).first()
    # print(book.publish)

    # 查询书籍主键为2的作者
    # book = models.Book.objects.filter(pk=2).first()
    # print(book.authors.all())

    # 查询作者张三的电话号码
    # author = models.Author.objects.filter(name='张三').first()
    # print(author.detail.mobile)

    #### 基于子查询的反向查询  表名小写  查询出多个需要+set：book_set
    # 查询东方出版社出版的书
    # publisher = models.Publish.objects.filter(name='东方出版社').first()
    # print(publisher.book_set.all())

    # 查询作者为张三的书
    # author = models.Author.objects.filter(name='张三').first()
    # print(author.book_set.all())

    # 查询手机号是110的作者姓名
    # author_detail = models.Author_detail.objects.filter(mobile='110').first()
    # print(author_detail.author) #一对一不需要+set

    #### 基于双下划线的正向查询
    # 查询书籍主键为1的出版社名称
    # publish = models.Book.objects.filter(pk=1).values('publish__name')
    # print(publish)

    # 查询书籍主键为2的作者
    # authors = models.Book.objects.filter(pk=2).values('authors__name')
    # print(authors)

    # 查询作者张三的电话号码
    # author_detail = models.Author.objects.filter(name='张三').values('detail__mobile')
    # print(author_detail)
    # mobile = models.Author_detail.objects.filter(author__name='张三').values('mobile')
    # print(mobile)

    #### 基于双下划线的反向查询  表名小写  查询出多个需要+set：book_set
    # 查询东方出版社出版的书
    # books = models.Publish.objects.filter(name='东方出版社').values('book__name')
    # print(books)

    # 查询作者为张三的书
    # books = models.Author.objects.filter(name='张三').values('book__name')
    # print(books)

    # 查询手机号是110的作者姓名
    # author = models.Author_detail.objects.filter(mobile='110').values('author__name')
    # print(author)

    # 查询书籍主键是1的作者的手机号
    # mobile = models.Author_detail.objects.filter(author__book__pk=1).values('mobile')
    # mobile = models.Book.objects.filter(pk=1).values('authors__detail__mobile')
    # print(mobile)

    '''
    聚合查询   不分组 使用aggregate
    '''
    # avgPrice = models.Book.objects.aggregate(Avg('price'),Max('price'),Min('price'),Sum('price'),Count('price'))
    # print(avgPrice)
    # 统计每本书的作者个数  annotate前面是什么就按什么分组
    # obj = models.Book.objects.values('name').annotate(authorNum=Count('authors'))
    # print(obj)
    # 统计每个出版社买的最便宜的书的价格
    # mins = models.Publish.objects.values('name').annotate(minPrice=Min('book__price')).values('name', 'minPrice')
    # print(mins)
    # 统计不只一个作者的图书
    # book = models.Book.objects.annotate(countAuthors=Count('authors')).filter(countAuthors__gt=1).values('name','countAuthors')
    # print(book)
    # 查询每个作者出的书的总价格
    # price = models.Author.objects.annotate(price_sum=Sum('book__price')).values('name', 'price_sum')
    # print(price)

    '''
    F与Q查询
    '''
    """F查询 直接获取表中字段的数据"""
    # 1 查询卖出数大于库存数的书籍
    from django.db.models import F
    # res = models.Book.objects.filter(maichu__gt=F('kucun'))
    # print(res)
    # 2 将所有书籍的价格提升50元
    # update = models.Book.objects.update(price=F('price') + 50)
    # print(update)
    # 3 将所有书籍的名称后面加上'爆款'
    # update = models.Book.objects.update(name=Concat(F('name'), Value('爆款')))
    # print(update)
    """Q查询"""
    # 1 查询卖出数大于800或价格小于150的书籍
    # book = models.Book.objects.filter(Q(maichu__gt=800), Q(price__lt=150)) # Q包裹','分割还是and关系
    # book = models.Book.objects.filter(Q(maichu__gt=800)| Q(price__lt=150)) # 或
    # book = models.Book.objects.filter(Q(maichu__gt=800)| ~Q(price__lt=150)) # 非~
    # print(book)

    # Q的高阶用法 能够将查询条件的左边也变成字符串形式   例如：根据用户输入的key作为筛选条件的左边
    q= Q()
    q.connector = 'OR'
    q.children.append(('maichu__gt',800))
    q.children.append(('price__lt',150))
    res = models.Book.objects.filter(q)
    print(res)


if __name__ == '__main__':
    main()
