from django.contrib import admin

from training_system import models

# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.Lesson)
admin.site.register(models.Group)
admin.site.register(models.Subscription)

