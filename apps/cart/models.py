import uuid

from django.db import models

from apps.product.models import Product
from apps.user.models import User


class CartManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user').prefetch_related('cartitem_set__product')

    def get_or_create_user_cart(self, request):
        return self._get_user_cart(request, create_if_missing=True)

    def get_or_none_user_cart(self, request):
        return self._get_user_cart(request, create_if_missing=False)

    def merge_cart(self, request):
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            session_cart = self.filter(id=session_cart_id, user=None).first()
            if session_cart:
                user_cart = self.get(user=request.user)
                for item in session_cart.cartitem_set.all():
                    CartItem.objects.create(cart=user_cart, product=item.product, quantity=item.quantity)
                session_cart.delete()
                del request.session['cart_id']
                request.session.modified = True
        return user_cart

    def clear_cart(self, request):
        cart = self.get_or_none_user_cart(request)
        if cart:
            cart.products.clear()
        return cart

    def _get_user_cart(self, request, create_if_missing):
        if request.user.is_authenticated:
            cart = self.get(user=request.user)
        else:
            session_cart_id = request.session.get('cart_id')
            if session_cart_id:
                cart = self.filter(id=session_cart_id, user=None).first()
            elif create_if_missing:
                cart = Cart.objects.create(user=None)
                request.session['cart_id'] = cart.id
                request.session.modified = True
            else:
                return None
        return cart


class CartItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('cart', 'product')

    def add_product_to_cart(self, cart, product_id, quantity=1):
        product = Product.objects.get(id=product_id)
        cart_item, created = self.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity if not created else quantity
        cart_item.save()
        return cart_item

    def remove_product_from_cart(self, cart, product_id):
        product = Product.objects.get(id=product_id)
        self.filter(cart=cart, product=product).delete()

    def update_product_quantity(self, cart, product_id, quantity):
        product = Product.objects.get(id=product_id)
        cart_item = self.get(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()
        return cart_item


class Cart(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    objects = CartManager()

    def get_total_price(self):
        return sum(item.product.get_discounted_price() * item.quantity for item in self.cartitem_set.all())

    class Meta:
        indexes = [
            models.Index(fields=['public_id']),
            models.Index(fields=['user'])
        ]

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    objects = CartItemManager()

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

    class Meta:
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product'])
        ]
