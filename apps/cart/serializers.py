from rest_framework import serializers

from apps.cart.models import Cart, CartItem
from apps.product.models import Product


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        exclude = ['id', ]

    def get_items(self, obj):
        return CartItemSerializer(obj.cartitem_set.all(), many=True).data

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        exclude = ['id', 'cart']


class CartItemActionSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1, required=False, default=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product with this ID does not exist.")
        return value

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
