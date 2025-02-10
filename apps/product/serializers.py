from rest_framework import serializers

from apps.product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['public_id', 'name', 'price', 'discount', 'get_discounted_price']
        read_only_fields = ['get_discounted_price']
