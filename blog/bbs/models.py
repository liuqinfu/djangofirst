from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# 用户表
class User(AbstractUser):
    phone = models.CharField(max_length=11, null=True, verbose_name='手机号')
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.jpg', verbose_name='头像')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    site = models.OneToOneField(to='Site', null=True, on_delete=models.DO_NOTHING)


# 站点表
class Site(models.Model):
    name = models.CharField(max_length=100, verbose_name='站点名称')
    title = models.CharField(max_length=100, verbose_name='站点标题')
    theme = models.CharField(max_length=64, verbose_name='个人站点样式')  # 存css或js的文件路径  简单模拟


# 标签表
class Label(models.Model):
    name = models.CharField(max_length=50, verbose_name='标签名')
    site = models.ForeignKey(to='Site',null=True, on_delete=models.CASCADE)


# 类别表
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='分类名')
    site = models.ForeignKey(to='Site',null=True, on_delete=models.CASCADE)


# 文章表
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=100, verbose_name='文章简介')
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    up_num = models.BigIntegerField(verbose_name='点赞数')
    down_num = models.BigIntegerField(verbose_name='点踩数')
    comment_num = models.BigIntegerField(verbose_name='评论数')
    site = models.ForeignKey(to='Site', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(to='Category', on_delete=models.DO_NOTHING)
    labels = models.ManyToManyField(to='Label',through='Article2Label',through_fields=('article','label'))

class Article2Label(models.Model):
    article = models.ForeignKey(to='Article',on_delete=models.CASCADE)
    label = models.ForeignKey(to='Label',on_delete=models.CASCADE)

# 点赞点踩表
class Updown(models.Model):
    user = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    is_up = models.BooleanField(verbose_name='是否是点赞')
    create_time = models.DateTimeField(verbose_name='操作时间', auto_now_add=True)


# 评论表
class Comment(models.Model):
    user = models.ForeignKey(to='User', on_delete=models.DO_NOTHING)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)
    content = models.CharField(max_length=255, verbose_name='评论内容')
    create_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    # 自关联
    # parent = models.ForeignKey(to='Comment',null=True,on_delete=models.CASCADE)
    parent = models.ForeignKey(to='self', null=True, on_delete=models.CASCADE)
