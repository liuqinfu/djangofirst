# Generated by Django 3.1 on 2020-09-11 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmanage', '0007_auto_20200906_0441'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='gender',
            field=models.IntegerField(choices=[(1, '男'), (2, '女'), (3, '未知')], null=True),
        ),
    ]