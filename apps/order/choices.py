from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = ('Pending', 'Pending', )
    PENDING_COD = ('pending_cod', 'Pending COD', )
    PAID = ('Paid', 'Paid', )
    SHIPPED = ('Shipped', 'Shipped', )
    DELIVERED = ('Delivered', 'Delivered', )
    FAILED = ('Failed', 'Failed', )


class OrderDeliveryMethod(models.TextChoices):
    NOVA_POST = ('nova_post', 'Nova post', )
    UKR_POST = ('ukr_post', 'Ukrposhta', )
    PICKUP = ('pickup', 'Pickup', )


class OrderPaymentMethod(models.TextChoices):
    CREDIT_CARD = ('credit_card', 'Credit Card', )
    CASH_ON_DELIVERY = ('cash_on_delivery', 'Cash on Delivery', )
