import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from training_system import models, tasks


@receiver(post_save, sender=models.Subscription)
def subscribe(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        product = instance.product_id

        groups = models.Group.objects.filter(product_id=product)

        for group in groups:
            if group.students.count() < group.max_users:
                group.students.add(user)
                return

        new_group = models.Group.objects.create(
            group_name=f'Новая поток от {datetime.datetime.now()} Автор продукта {product.author}',
            product_id=product

        )

        new_group.students.add(user)
