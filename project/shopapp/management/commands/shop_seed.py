from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from shopapp.models import Product, Customer, Warehouse


class Command(BaseCommand):
    help = "Creates demo users, products, customers and warehouse data."

    def handle(self, *args, **options):
        User = get_user_model()

        self.create_admin(User)
        self.create_users(User)
        products = self.create_products()
        self.create_customers()
        self.create_warehouse(products)

        self.stdout.write(self.style.SUCCESS("Seed completed successfully."))

    def create_admin(self, User):
        username = "admin"

        if User.objects.filter(username=username).exists():
            self.stdout.write("Admin already exists.")
            return

        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
        )

        self.stdout.write(
            self.style.SUCCESS("Created admin: admin / admin")
        )

    def create_users(self, User):
        users = [
            {
                "username": "shopper1",
                "email": "shopper1@example.com",
                "password": "shopper1",
            },
            {
                "username": "shopper2",
                "email": "shopper2@example.com",
                "password": "shopper2",
            },
        ]

        for user_data in users:
            username = user_data["username"]

            if User.objects.filter(username=username).exists():
                self.stdout.write(f"User {username} already exists.")
                continue

            User.objects.create_user(
                username=username,
                email=user_data["email"],
                password=user_data["password"],
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created user: {username} / {user_data['password']}"
                )
            )

    def create_products(self):
        products_data = [
            {
                "name": "Czarne buty skórzane",
                "price": Decimal("299.99"),
                "description": "Eleganckie buty skórzane do codziennego użytku.",
                "stock": 10,
            },
            {
                "name": "Białe sneakersy",
                "price": Decimal("199.99"),
                "description": "Lekkie miejskie sneakersy.",
                "stock": 15,
            },
            {
                "name": "Buty trekkingowe",
                "price": Decimal("349.99"),
                "description": "Wytrzymałe buty do spacerów i wyjazdów.",
                "stock": 5,
            },
            {
                "name": "Czerwone trampki",
                "price": Decimal("149.99"),
                "description": "Casualowe trampki w czerwonym kolorze.",
                "stock": 20,
            },
            {
                "name": "Czarne mokasyny",
                "price": Decimal("249.99"),
                "description": "Minimalistyczne mokasyny półformalne.",
                "stock": 0,
            },
        ]

        created_products = []

        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data["name"],
                defaults={
                    "price": data["price"],
                    "description": data["description"],
                    "stock": data["stock"],
                },
            )

            if not created:
                product.price = data["price"]
                product.description = data["description"]
                product.stock = data["stock"]
                product.save()

            created_products.append(product)

            message = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(f"{message} product: {product.name}")
            )

        return created_products

    def create_customers(self):
        customers_data = [
            {
                "name": "Shopper One",
                "email": "shopper1@example.com",
            },
            {
                "name": "Shopper Two",
                "email": "shopper2@example.com",
            },
        ]

        for data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=data["email"],
                defaults={
                    "name": data["name"],
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created customer: {customer.name}")
                )
            else:
                self.stdout.write(f"Customer {customer.name} already exists.")

    def create_warehouse(self, products):
        warehouse, created = Warehouse.objects.get_or_create(
            location="Main Warehouse",
        )

        warehouse.products.set(products)

        if created:
            self.stdout.write(
                self.style.SUCCESS("Created warehouse: Main Warehouse")
            )
        else:
            self.stdout.write("Updated warehouse: Main Warehouse")