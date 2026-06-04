from django.db import models

# Create your models here.


class Product(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    # product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name
    
class Order(models.Model):

    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_date:%Y-%m-%d %H:%M} - {self.customer.name}"
    
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    #gwarancja unkalności produktów w zamówieniu
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_product_per_order"
            )
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Customer(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


