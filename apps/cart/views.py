from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.cart.models import CartItem, Cart
from apps.cart.serializers import CartSerializer, CartItemSerializer, CartItemActionSerializer
from apps.product.models import Product


@extend_schema(tags=['Carts'])
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects
    # http_method_names = ['get', 'post', 'delete']
    permission_classes = [AllowAny]
    serializer_class = CartSerializer

    def get_object(self):
        return self.queryset.get_or_none_user_cart(self.request)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def merge_cart(self, request):
        """
        Merge anonymous user cart with registered one's after they're logged in
        """
        self.queryset.merge_cart(request)
        return Response({'status': 'Cart merged'})

    @action(detail=False, methods=['delete'])
    def clear_cart(self, request):
        self.queryset.clear_cart()
        return Response({'status': 'Cart cleared'})


@extend_schema(tags=['Carts'])
class CartItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Cart items management (CartItem).
    """
    # http_method_names = ['get', 'post', 'delete', 'patch', ]
    serializer_class = CartItemSerializer

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        serializer = CartItemActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = Cart.objects.get_or_create_user_cart(request)
        cart_item = CartItem.objects.add_product_to_cart(
            cart, serializer.validated_data['product_id'], serializer.validated_data['quantity'],
        )

        response_data = CartItemSerializer(cart_item).data
        return Response(response_data)

    @action(detail=False, methods=['delete'])
    def remove_product(self, request):
        serializer = CartItemActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = Cart.objects.get_or_none_user_cart(request)
        CartItem.objects.remove_product_from_cart(cart, serializer.validated_data['product_id'])

        return Response({'status': 'Product removed'})

    @action(detail=False, methods=['patch'])
    def update_quantity(self, request):
        serializer = CartItemActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = Cart.objects.get_or_none_user_cart(request)
        cart_item = CartItem.objects.update_product_quantity(
            cart, serializer.validated_data['product_id'], serializer.validated_data['quantity'],
        )

        response_data = CartItemSerializer(cart_item).data
        return Response(response_data)


# TODO check logic inside views
# TODO maybe there need to add and check product availability but not sure
