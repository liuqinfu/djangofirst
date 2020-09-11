import django
from django.db import models


# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=50, verbose_name='书名')
    # 小数总共8位，小数点后占两位，即：整数部分占6位
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='价格')
    publish = models.ForeignKey(to='Publish', on_delete=models.CASCADE)
    authors = models.ManyToManyField(to='Author')
    publishTime = models.DateField(auto_now_add=True)
    maichu = models.IntegerField(default=1000,verbose_name='卖出')
    kucun = models.IntegerField(default=1000,verbose_name='库存')

    def __str__(self):
        return self.name


class Publish(models.Model):
    name = models.CharField(max_length=50, verbose_name='出版社名称')
    addr = models.CharField(max_length=20, verbose_name='所在地')

    def __str__(self):
        return '对象：%s' % self.name


gender_choices = [
    (1,'男'),
    (2,'女'),
    (3,'未知')
]

class Author(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    gender = models.IntegerField(choices=gender_choices,null=True)
    detail = models.OneToOneField(to='Author_detail', on_delete=models.CASCADE)



class Author_detail(models.Model):
    mobile = models.BigIntegerField(verbose_name='手机号')
    addr = models.CharField(max_length=50, verbose_name='住址')
    email = models.EmailField(null=True)
