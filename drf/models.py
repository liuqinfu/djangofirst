
# Create your models here.
from django.db import models
from django.db.models import Model


class Student(Model):
    name = models.CharField(max_length=10, verbose_name='用户名')
    age = models.IntegerField(default=20, verbose_name='年龄')
