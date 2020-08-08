from django.db import models


# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=50, verbose_name='书名')
    # 小数总共8位，小数点后占两位，即：整数部分占6位
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='价格')
    publish = models.ForeignKey(to='Publish', on_delete=models.CASCADE)
    authors = models.ManyToManyField(to='Author')


class Publish(models.Model):
    name = models.CharField(max_length=50, verbose_name='出版社名称')
    addr = models.CharField(max_length=20, verbose_name='所在地')


class Author(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    detail = models.OneToOneField(to='Author_detail', on_delete=models.CASCADE)


class Author_detail(models.Model):
    mobile = models.BigIntegerField(verbose_name='手机号')
    addr = models.CharField(max_length=50, verbose_name='住址')
