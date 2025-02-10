from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from apps.order.models import Order
from apps.order.serializers import OrderSerializer, CheckoutSerializer, OrderStatusChangeSerializer
from apps.order.services.checkout import CheckoutService
from apps.order.services.order import OrderService


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

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def checkout(self, request):
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        order_service = OrderService()
        order = order_service.create_order_from_cart(request, serializer.validated_data)

        try:
            checkout_service = CheckoutService()
            result = checkout_service.process_checkout(order)
            return Response(result)
        except ValueError as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)

    @action(detail=True, methods=['post'], url_path='change-status', permission_classes=[IsAdminUser])
    def change_status(self, request, pk=None):
        """
        Endpoint for making manual order status change on SHIPPED or DELIVERED, by admin users
        """
        order = self.get_object()
        serializer = OrderStatusChangeSerializer(data=request.data, context={'order': order})
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        order_service = OrderService()
        order = order_service.change_status(order, new_status)

        return Response({"status": "success", "new_status": order.status})

    @action(detail=True, methods=['get'], url_path='track-status', permission_classes=[AllowAny])
    def track(self, request, pk=None):
        order = self.get_object()
        return Response({'tracking_status': order.status})
