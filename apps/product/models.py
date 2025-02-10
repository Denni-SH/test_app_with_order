import uuid

from django.db import models


class Product(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def get_discounted_price(self):
        return self.price * (1 - self.discount / 100)

    class Meta:
        indexes = [
            models.Index(fields=['public_id']),
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return f"Product \"{self.name}\""
