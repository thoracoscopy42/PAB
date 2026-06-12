from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from .models import Product, Order, OrderItem, Customer


@transaction.atomic
def create_order_atomic(cart: dict) -> Order:
    if not cart:
        raise ValidationError("Koszyk jest pusty.")

    customer = Customer.objects.first()

    if customer is None:
        raise ValidationError("Brak klienta w bazie danych.")

    order = Order.objects.create(
        customer=customer
    )

    for product_id_as_string, quantity in cart.items():
        product_id = int(product_id_as_string)

        if quantity <= 0:
            raise ValidationError("Ilość produktu musi być większa od zera.")

        product = Product.objects.select_for_update().get(pk=product_id)

        if product.stock < quantity:
            raise ValidationError(
                f"Brak wystarczającej ilości produktu: {product.name}."
            )

        Product.objects.filter(pk=product.pk).update(
            stock=F("stock") - quantity
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

    return order