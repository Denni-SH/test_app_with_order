from abc import ABC, abstractmethod


class PaymentServiceInterface(ABC):
    @abstractmethod
    def create_payment_link_response(self, order):
        """
        Create order payment link
        """
        pass

    @abstractmethod
    def handle_payment_webhook(self, event):
        """
        Handle payment system webhook about payment results
        """
        pass
