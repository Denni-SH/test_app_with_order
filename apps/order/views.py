from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.order.models import Order, OrderItem
from apps.order.serializers import OrderSerializer


@extend_schema(tags=['Orders'])
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['status']
    ordering_fields = ['status']
    ordering = ['status']
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.with_related().filter(user=self.request.user)

    # TODO: review if can be improved: like move orderitem creation to order save or signals, so as cart deletion
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        cart = self.request.user.cart_set.with_related().get(id=pk)
        order = Order.objects.create(
            user=cart.user,
            address=request.data['address'],
            delivery_method=request.data['delivery_method'],
            payment_method=request.data['payment_method']
        )
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.delete()
        return Response({'status': 'Order placed', 'order_id': order.id})

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        order = self.get_object()
        order.process_payment()
        return Response({'status': 'Payment processed'})

    @action(detail=True, methods=['get'])
    def track(self, request, pk=None):
        order = self.get_object()
        return Response({'tracking_status': order.track_order()})
