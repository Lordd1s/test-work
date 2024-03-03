from celery import shared_task
from datetime import datetime
import time

from django.db.models import QuerySet
from django.utils import timezone

from training_system import models


@shared_task
def start():
    products: QuerySet = models.Product.objects.filter(start_date__gte=timezone.now())
    # print(products)
    if products.exists():
        for product in products:
            upd_group(product)
    else:
        print('Product not exists')
    return None


@shared_task
def upd_group(instance):
    # Получение групп по продукту! instance - это объект Product
    groups: QuerySet = models.Group.objects.filter(product_id=instance.id).prefetch_related('product_id')

    # Временное сохранение студентов
    students_qs = list(x.students.values_list('id', flat=True) for x in groups)  # QuerySets with id of students
    students = []  # Id of students

    for i in students_qs:
        for j in i:
            # print(j)
            students.append(j)

    students.sort()
    # print(students)

    # Общее кол-во студентов
    total_students = sum(group.students.count() for group in groups)

    max_students_per_group = 10

    # Студент к каждой группе
    students_per_group = total_students // groups.count()

    # Если не хватает студентов! (25 // 3 == 8) (8 * 3 != 25) (25 - 24 = 1 - это оставшиеся студент которая не рспределяется!)
    missing_student = 0
    missed = []
    if students_per_group != int(groups.count() * students_per_group):
        missing_student = total_students % students_per_group
        missed = [students[missing_student]]
        del students[missing_student]
        print(missing_student)

    # Перераспределение студентов на группы!
    for group in groups:
        # print(group.students.all())
        # print('starting 1')
        if group.students.count() <= max_students_per_group:
            # print('in progress')
            group.students.set(students[:students_per_group])
            del students[:students_per_group]
        #     print(students)

        if missing_student > 0:
            # print("starting 2")
            group.students.add(*missed)
            missing_student -= 1
            # print("Student added (missing_student)")

    for gr in groups:
        if gr.students.count() == 0:
            # print(gr.students)
            gr.delete()
    print('done')

    return "Students redistributed successfully."
