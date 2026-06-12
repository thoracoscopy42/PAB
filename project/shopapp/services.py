from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from .models import Product, Order


@transaction.atomic
def create_order_atomic(product_id: int, quantity: int) -> Order:
    if quantity <= 0:
        raise ValidationError("Ilość musi być większa od zera.")

    product = Product.objects.select_for_update().get(pk=product_id)

    if product.stock < quantity:
        raise ValidationError("Brak wystarczającej ilości produktu w magazynie.")

    Product.objects.filter(pk=product.pk).update(
        stock=F("stock") - quantity
    )

    order = Order.objects.create(
        product=product,
        quantity=quantity
    )

    return order