from django.dispatcher import receiver
from store.signals import order_created


@receiver(order_created)
def after_oder_created(senderm, **kwargs):
    print(f'New order is created {kwargs["order"].id}')