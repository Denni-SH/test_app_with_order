from apps.order.choices import OrderPaymentMethod, OrderStatus
from apps.order.services.order import OrderService
from apps.order.services.square import SquareService


class PaymentProcessor:
    def process_payment(self, order):
        raise NotImplementedError("This method should be implemented by subclasses.")


class CreditCardPaymentProcessor(PaymentProcessor):
    def process_payment(self, order):
        print(f"Processing credit card payment for Order {order.id}")

        payment_service = SquareService()
        payment_link = payment_service.create_payment_link_response(order)

        return {
            "order_id": order.public_id, "payment_link": payment_link,
            "status": "success", "message": "Payment processed via credit card."
        }


class CashOnDeliveryPaymentProcessor(PaymentProcessor):
    def process_payment(self, order):
        print(f"Processing Cash on Delivery for Order {order.id}")

        order_service = OrderService()
        order_service.change_status(OrderStatus.PENDING_COD)
        return {
            "status": "success",
            "message": "Cash on Delivery selected. Awaiting delivery and payment."
        }


class PaymentProcessorFactory:
    _processors = {
        OrderPaymentMethod.CREDIT_CARD: CreditCardPaymentProcessor,
        OrderPaymentMethod.CASH_ON_DELIVERY: CashOnDeliveryPaymentProcessor,
    }

    @classmethod
    def get_processor(cls, payment_method):
        processor_class = cls._processors.get(payment_method)
        if not processor_class:
            raise ValueError(f"No payment processor found for method {payment_method}")
        return processor_class()


