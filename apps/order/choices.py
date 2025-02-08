from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = ('Pending', 'Pending', )
    PAID = ('Paid', 'Paid', )
    SHIPPED = ('Shipped', 'Shipped', )
    DELIVERED = ('Delivered', 'Delivered', )
    CANCELED = ('Canceled', 'Canceled', )
    FAILED = ('Failed', 'Failed', )
