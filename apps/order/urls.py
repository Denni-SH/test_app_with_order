from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import square_webhooks
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='orders')

urlpatterns = [
    path('payment-webhooks/square/', square_webhooks.order_payment_webhook, name='order_payment_webhook'),
    path('', include(router.urls)),
]
