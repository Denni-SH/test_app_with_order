from apps.order.services.payment import PaymentProcessorFactory


class CheckoutService:
    def process_checkout(self, order):
        processor = PaymentProcessorFactory.get_processor(order.payment_method)

        payment_result = processor.process_payment(order)
        if payment_result.get("status") != "success":
            raise ValueError("Payment failed: " + payment_result.get("message", "Unknown error"))

        return payment_result
