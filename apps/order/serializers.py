from rest_framework import serializers

from apps.order.choices import OrderDeliveryMethod, OrderPaymentMethod, OrderStatus
from apps.order.models import Order, OrderItem, ContactInfo


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_items(self, obj):
        return OrderItemSerializer(obj.orderitem_set.all(), many=True).data


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class CheckoutSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=500)
    delivery_method = serializers.ChoiceField(choices=OrderDeliveryMethod.choices)
    payment_method = serializers.ChoiceField(choices=OrderPaymentMethod.choices)

    def validate(self, data):
        user = self.context['request'].user
        cart = user.cart_set.first()
        if not cart or not cart.cartitem_set.exists():
            raise serializers.ValidationError("Your cart is empty.")
        return data


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']


class OrderStatusChangeSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)

    def validate_status(self, value):
        order = self.context['order']
        if not order.can_change_status_to(value):
            raise serializers.ValidationError(f"Cannot change status from {order.status} to {value}.")
        return value
