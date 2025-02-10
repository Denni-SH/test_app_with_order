from django.conf import settings
from django.shortcuts import get_object_or_404

from apps.order.choices import OrderStatus
from apps.order.models import Order
from apps.order.services.interfaces import PaymentServiceInterface
from apps.order.services.order import OrderService


class SquareService(PaymentServiceInterface):
    def __init__(self):
        from square.client import Client
        self.client = Client(
            access_token=settings.SQUARE_ACCESS_TOKEN,
            environment=settings.SQUARE_ENVIRONMENT_TYPE,
        )

    def create_payment_link_response(self, order):
        customer = self._get_or_create_customer(order.user)
        request_body = dict()  # Here is adding order_items, customer_id, redirect_url and pre_populated_data
        result = self.client.checkout.create_payment_link(body=request_body)

        # Here's a check response for success. Raise exception otherwise

        order.square_order_id = result.body['payment_link']['order_id']
        order.save()
        return result.body['payment_link']['url']

    def handle_payment_webhook(self, event):
        event_type = event.get('type')

        if event_type not in ['payment.succeeded', 'payment.failed', ]:
            # Here's the event_type check and exception raises
            pass

        order = get_object_or_404(Order, square_order_id=event['data']['object']['payment']['order_id'])
        new_status = OrderStatus.PAID if event_type == 'payment.succeeded' else OrderStatus.FAILED
        order_service = OrderService()
        order_service.change_status(order, new_status)

    def _get_or_create_customer(self, user):
        if hasattr(user, 'square_customer_id') and user.square_customer_id:
            return user.square_customer_id

        result = self.client.customers.create_customer(
            body={
                "given_name": user.first_name,
                "family_name": user.last_name,
                "email_address": user.email,
            }
        )

        # Here's a check response for success and raise exception otherwise
        square_customer_id = result.body['customer']['id']
        user.square_customer_id = square_customer_id
        user.save()
        return square_customer_id
