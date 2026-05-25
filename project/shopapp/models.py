from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order of {self.quantity} {self.product.name}(s) on {self.order_date}" 
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    location = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.location

