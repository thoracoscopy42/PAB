from django.contrib import admin

from .models import Product, Order, Customer, Warehouse
# Register your models here.


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Warehouse)