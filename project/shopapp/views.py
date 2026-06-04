
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Product




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

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "cart_unique_count": len(cart),
            "product_id": product.id,
            "quantity": cart[product_id_as_string],
        })

    return redirect("index")

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id_as_string = str(product_id)

    if product_id_as_string in cart:
        del cart[product_id_as_string]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart_detail")

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

def update_cart(request):
    if request.method == "POST":
        cart = request.session.get("cart", {})

        for product_id_as_string in list(cart.keys()):
            quantity_field_name = f"quantity_{product_id_as_string}"
            quantity_value = request.POST.get(quantity_field_name)

            if quantity_value:
                try:
                    quantity = int(quantity_value)
                except ValueError:
                    quantity = 1

                if quantity > 0:
                    cart[product_id_as_string] = quantity
                else:
                    del cart[product_id_as_string]

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart_detail")