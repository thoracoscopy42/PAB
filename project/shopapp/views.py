from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


from django.shortcuts import render

from .models import Product


def index(request):
    products = Product.objects.all().order_by("name")

    return render(
        request,
        "shopapp/index.html",
        {
            "products": products,
        }
    )