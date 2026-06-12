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
    #zmiana ilości w koszyku
    path("cart/change/<int:product_id>/<str:action>/", views.change_cart_item, name="change_cart_item"),
    path("checkout/", views.checkout, name="checkout"),
]