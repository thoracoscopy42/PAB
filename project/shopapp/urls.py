from django.urls import path
from . import views

#ig do obrazków 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    #sam koszyk
    path("cart/", views.cart_detail, name="cart_detail"),
    #dodawanie produktu do koszyka
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    # usuwanie i update
    path("cart/update/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
]