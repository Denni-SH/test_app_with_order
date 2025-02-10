from apps.cart.models import Cart
from apps.order.models import Order, OrderItem
from apps.order.serializers import ContactInfoSerializer
from apps.order.tasks import send_order_status_email


class OrderService:
    def change_status(self, order, new_status):
        if not order.can_change_status_to(new_status):
            raise ValueError(f"Cannot change status from {order.status} to {new_status}.")

        order.status = new_status
        order.save()
        send_order_status_email.delay(order.id)
        return order

    @staticmethod
    def create_order_from_cart(request, validated_data):
        cart = Cart.objects.get_or_none_user_cart(request)
        if not cart or not cart.cartitem_set.exists():
            raise ValueError("Cart is empty or not found for the user.")

        contact_info_serializer = ContactInfoSerializer(
            data={
                'first_name': validated_data['first_name'],
                'last_name': validated_data['last_name'],
                'email': validated_data['email'],
                'phone': validated_data['phone'],
                'address': validated_data['address']
            }
        )
        contact_info_serializer.is_valid(raise_exception=True)
        contact_info = contact_info_serializer.save()

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            contact_info=contact_info,
            delivery_method=validated_data['delivery_method'],
            payment_method=validated_data['payment_method']
        )
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.products.clear()
        return order
