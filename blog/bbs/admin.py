from django.contrib import admin

# Register your models here.

from bbs import models

admin.site.register(models.User)
admin.site.register(models.Article)
admin.site.register(models.Article2Label)
admin.site.register(models.Category)
admin.site.register(models.Label)
admin.site.register(models.Comment)
admin.site.register(models.Site)
admin.site.register(models.Updown)