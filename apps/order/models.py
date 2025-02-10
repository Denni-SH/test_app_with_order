import uuid

from django.db import models

from apps.order.choices import OrderStatus, OrderDeliveryMethod, OrderPaymentMethod
from apps.product.models import Product
from apps.user.models import User


class OrderManager(models.Manager):
    def with_related(self):
        return self.get_queryset().select_related('user').prefetch_related('orderitem_set__product')


class ContactInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.email})"


class Order(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    delivery_method = models.CharField(max_length=100, choices=OrderDeliveryMethod.choices)
    payment_method = models.CharField(max_length=100, choices=OrderPaymentMethod.choices)
    square_order_id = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    VALID_TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.PAID, OrderStatus.FAILED, OrderStatus.PENDING_COD, ],
        OrderStatus.PENDING_COD: [OrderStatus.SHIPPED, ],
        OrderStatus.PAID: [OrderStatus.SHIPPED, ],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED, ],
        OrderStatus.DELIVERED: [],
        OrderStatus.FAILED: [],
    }

    objects = OrderManager()

    class Meta:
        indexes = [
            models.Index(fields=['public_id']),
            models.Index(fields=['user']),
            models.Index(fields=['status'])
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.status = OrderStatus.PENDING
        super().save(*args, **kwargs)

    def can_change_status_to(self, new_status):
        """
        Checks whether a transition to a new status is possible.
        """
        return new_status in self.VALID_TRANSITIONS[self.status]


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
