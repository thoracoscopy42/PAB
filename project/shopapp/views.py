
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

from .models import Product
from .services import create_order_atomic




def index(request):
    products = Product.objects.all().order_by("name")

    cart = request.session.get("cart", {})
    cart_unique_count = len(cart)

    return render(
        request,
        "shopapp/index.html",
        {
            "products": products,
            "cart_unique_count": cart_unique_count,
        }
    )

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})
    product_id_as_string = str(product.id)

    if product_id_as_string in cart:
        cart[product_id_as_string] += 1
    else:
        cart[product_id_as_string] = 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("index")

def cart_detail(request):
    cart = request.session.get("cart", {})

    product_ids = cart.keys()

    products = Product.objects.filter(id__in=product_ids)

    cart_items = []

    for product in products:
        product_id_as_string = str(product.id)

        cart_items.append({
            "product": product,
            "quantity": cart[product_id_as_string],
        })

    cart_unique_count = len(cart)

    return render(
        request,
        "shopapp/cart_detail.html",
        {
            "cart_items": cart_items,
            "cart_unique_count": cart_unique_count,
        }
    )

def change_cart_item(request, product_id, action):
    cart = request.session.get("cart", {})

    product_id_as_string = str(product_id)

    if product_id_as_string in cart:
        if action == "increase":
            cart[product_id_as_string] += 1

        elif action == "decrease":
            cart[product_id_as_string] -= 1

            if cart[product_id_as_string] <= 0:
                del cart[product_id_as_string]

        elif action == "remove":
            del cart[product_id_as_string]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart_detail")


@require_POST
def create_order_view(request):
    product_id = int(request.POST["product_id"])
    quantity = int(request.POST["quantity"])

    try:
        order = create_order_atomic(product_id=product_id, quantity=quantity)
    except ValidationError as error:
        return HttpResponse(str(error), status=400)

    return HttpResponse(f"Utworzono zamówienie #{order.id}")