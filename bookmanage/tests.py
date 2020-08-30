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
    objects_filter = models.Publish.objects.filter(addr='宋朝')
    first = objects_filter.first()
    first.addr = '宋朝'
    update = first.save()


if __name__ == '__main__':
    main()