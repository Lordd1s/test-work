from django.contrib import admin

from training_system import models

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ("author", "product_name", "start_date", "cost")
    list_filter = ("author", "start_date", "cost")
    search_fields = ("author", "start_date", "cost")


admin.site.register(models.Product, ProductAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ("product_id", "lesson_name", "video_url")
    list_filter = ("product_id", )
    search_fields = ("product_id", "lesson_name")


admin.site.register(models.Lesson, LessonAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ("group_name", "product_id", "students", "max_users", "min_users")
    list_filter = ("group_name", "product_id", "max_users", "min_users")
    search_fields = ("group_name", "product_id", "max_users", "min_users")


admin.site.register(models.Group, GroupAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "product_id", "start_date", "end_date")
    list_filter = ("product_id", "start_date", "end_date")
    search_fields = ("product_id", "start_date", "end_date")


admin.site.register(models.Subscription, SubscriptionAdmin)
