from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=10,verbose_name='用户名')
    age = models.IntegerField(verbose_name='年龄',null=True)
    sex = models.CharField(max_length=2,verbose_name='性别')
    password = models.CharField(max_length=50,default='1234',verbose_name='密码')