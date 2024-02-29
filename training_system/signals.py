import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save

from training_system import models


@receiver(post_save, sender=models.Subscription)
def subscribe(instance, created, **kwargs):
    if created:
        print('starting')
        user = instance.user
        product = instance.product

        groups = models.Groupp.objects.filter(product_id=product)
        print('processing')
        for group in groups:
            if group.students.count() < group.max_users:
                group.students.add(user)
                return

        new_group = models.Groupp.objects.create(
            group_name=f'Новая поток от {datetime.datetime.today} Автор продукта {product.author}'

        )

        new_group.students.add(user)
        print('Added')
