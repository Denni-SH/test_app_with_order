import uuid

from django.db import models

from apps.order.choices import OrderStatus
from apps.product.models import Product
from apps.user.models import User


class OrderManager(models.Manager):
    def with_related(self):
        return self.get_queryset().select_related('user').prefetch_related('orderitem_set__product')


class Order(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    address = models.TextField()
    delivery_method = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)

    objects = OrderManager()

    def process_payment(self):
        self.status = OrderStatus.PAID
        self.save()
        self.send_order_to_external_system()

    def send_order_to_external_system(self):
        print("Order sent to external system")

    def track_order(self):
        return "In Transit"

    class Meta:
        indexes = [
            models.Index(fields=['public_id']),
            models.Index(fields=['user']),
            models.Index(fields=['status'])
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product'])
        ]
