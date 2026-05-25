from django.contrib import admin

from .models import Product, Order, Customer, Warehouse
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "description", "stock")
    search_fields = ("name",)
    list_filter = ("price",)