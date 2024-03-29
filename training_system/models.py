from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    author = models.ForeignKey(verbose_name="Автор", to=User, on_delete=models.CASCADE)
    product_name = models.CharField(verbose_name="Имя продукта", max_length=200)
    start_date = models.DateTimeField(verbose_name="Дата и время старта!", null=True)
    cost = models.FloatField(verbose_name="Цена")

    class Meta:
        app_label = 'training_system'
        ordering = ('-start_date', 'cost', 'author')
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.product_name}, автор: {self.author.first_name}, дата старта: {self.start_date}'


class Lesson(models.Model):
    product_id = models.ForeignKey(to=Product, on_delete=models.DO_NOTHING, related_name='product_lessons')
    video_url = models.TextField(verbose_name="Ссылка на видео!")
    lesson_name = models.CharField(verbose_name="Название урока", max_length=200)

    class Meta:
        app_label = 'training_system'
        ordering = ('lesson_name', 'product_id')
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'Урок {self.lesson_name}'


class Group(models.Model):
    students = models.ManyToManyField(to=User, related_name='students')
    group_name = models.CharField(verbose_name="Название группы", max_length=100)
    product_id = models.ForeignKey(to=Product, on_delete=models.DO_NOTHING, related_name="product")
    max_users = models.PositiveIntegerField(verbose_name="Максимальное количество студентов", default=10)
    min_users = models.PositiveIntegerField(verbose_name="Минимальное количество студентов", default=5)

    class Meta:
        app_label = 'training_system'
        ordering = ('group_name', 'max_users',)
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.group_name


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')
    product_id = models.ForeignKey(to=Product, on_delete=models.DO_NOTHING, related_name="products")
    start_date = models.DateTimeField(verbose_name="Начало подписки", default=timezone.now)
    end_date = models.DateTimeField(verbose_name="Окончание подписки", null=True)

    class Meta:
        app_label = 'training_system'
        ordering = ('-start_date',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'Пользователь {self.user.username} подписался на продукт {self.product_id.product_name}'
