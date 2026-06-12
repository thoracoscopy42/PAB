from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from .models import Product, Order, OrderItem


@transaction.atomic
def create_order_from_cart_atomic(cart: dict) -> Order:
    if not cart:
        raise ValidationError("Koszyk jest pusty.")

    order = Order.objects.create()

    for product_id_as_string, quantity in cart.items():
        quantity = int(quantity)

        if quantity <= 0:
            raise ValidationError("Ilość produktu musi być większa od zera.")

        product = Product.objects.select_for_update().get(
            pk=int(product_id_as_string)
        )

        if product.stock < quantity:
            raise ValidationError(
                f"Nie można zrealizować zamówienia. "
                f"Produkt: {product.name}. "
                f"W koszyku: {quantity} szt. "
                f"Dostępne na magazynie: {product.stock} szt."
            )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

        Product.objects.filter(pk=product.pk).update(
            stock=F("stock") - quantity
        )

    return order