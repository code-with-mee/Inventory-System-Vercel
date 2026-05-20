"""Seed the database with sample data: 20 records per app.

Usage:
    python manage.py seed_data          # top up each table to 20 records
    python manage.py seed_data --fresh  # wipe sample tables first, then seed
"""
import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from customers.models import Customer
from suppliers.models import Supplier
from products.models import Category, Product
from employees.models import Employee
from sales.models import Order, OrderDetail
from purchases.models import Purchase, PurchaseDetail

N = 20

FIRST = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael",
         "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan",
         "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
LAST = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Taylor", "Moore", "Jackson", "Martin", "Lee"]
CITIES = ["Phnom Penh", "Siem Reap", "Battambang", "Kampot", "Sihanoukville",
          "Kandal", "Takeo", "Pursat", "Kratie", "Prey Veng"]
SUPPLIER_NAMES = ["Global", "Prime", "Mekong", "Unity", "Summit", "Apex", "Delta",
                  "Pioneer", "Orient", "Crown", "Royal", "Star", "Pacific",
                  "Eastern", "Capital", "Premier", "Horizon", "Vista", "Nova",
                  "Atlas"]
SUPPLIER_SUFFIX = ["Trading Co.", "Distributors", "Supplies Ltd.", "Imports",
                   "Wholesale", "Enterprises", "Group", "Logistics"]
CATEGORIES = ["Electronics", "Beverages", "Snacks", "Dairy", "Bakery",
              "Frozen Foods", "Produce", "Meat", "Seafood", "Household",
              "Personal Care", "Stationery", "Toys", "Hardware", "Clothing",
              "Footwear", "Cosmetics", "Pet Supplies", "Health", "Automotive"]
PRODUCTS = ["Wireless Mouse", "Coffee Beans", "Potato Chips", "Fresh Milk",
            "Croissant", "Frozen Pizza", "Banana Bunch", "Chicken Breast",
            "Salmon Fillet", "Dish Soap", "Shampoo", "Notebook A5", "Toy Car",
            "Steel Hammer", "Cotton T-Shirt", "Running Shoes", "Lipstick",
            "Dog Food 5kg", "Vitamin C", "Engine Oil 1L"]
UNITS = ["pcs", "kg", "box", "pack", "bottle", "liter", "dozen"]


def phone():
    return "0" + str(random.randint(10000000, 99999999))


def address():
    return f"#{random.randint(1, 999)}, St. {random.randint(1, 600)}, {random.choice(CITIES)}"


class Command(BaseCommand):
    help = "Seed the database with 20 sample records per app."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh", action="store_true",
            help="Delete existing sample data before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)

        if options["fresh"]:
            OrderDetail.objects.all().delete()
            Order.objects.all().delete()
            PurchaseDetail.objects.all().delete()
            Purchase.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Customer.objects.all().delete()
            Supplier.objects.all().delete()
            Employee.objects.exclude(username="admin").delete()
            self.stdout.write("Cleared existing sample data.")

        # --- Customers ---
        for i in range(Customer.objects.count(), N):
            Customer.objects.create(
                name=f"{FIRST[i]} {LAST[i]}", phone=phone(), address=address())

        # --- Suppliers ---
        for i in range(Supplier.objects.count(), N):
            Supplier.objects.create(
                name=f"{SUPPLIER_NAMES[i]} {random.choice(SUPPLIER_SUFFIX)}",
                phone=phone(), address=address())

        # --- Categories ---
        for i in range(Category.objects.count(), N):
            Category.objects.create(name=CATEGORIES[i])

        # --- Employees (keep any existing, e.g. 'admin') ---
        existing_emp = Employee.objects.count()
        for i in range(existing_emp, N):
            Employee.objects.get_or_create(
                username=f"emp{i + 1:02d}",
                defaults=dict(
                    name=f"{FIRST[i]} {LAST[(i + 5) % N]}",
                    age=random.randint(21, 58),
                    phone=phone(),
                    address=address(),
                    password="pass1234",
                ),
            )

        # --- Products (need categories) ---
        categories = list(Category.objects.all())
        for i in range(Product.objects.count(), N):
            cost = Decimal(random.randint(50, 4000)) / Decimal(10)
            Product.objects.create(
                name=PRODUCTS[i],
                category=random.choice(categories),
                cost_price=cost,
                selling_price=(cost * Decimal("1.35")).quantize(Decimal("0.01")),
                unit=random.choice(UNITS),
            )

        customers = list(Customer.objects.all())
        suppliers = list(Supplier.objects.all())
        employees = list(Employee.objects.all())
        products = list(Product.objects.all())

        # --- Orders (sales) with 1-4 line items each ---
        for _ in range(Order.objects.count(), N):
            order = Order.objects.create(
                customer=random.choice(customers),
                employee=random.choice(employees),
            )
            for prod in random.sample(products, random.randint(1, 4)):
                OrderDetail.objects.create(
                    order=order, product=prod,
                    quantity=random.randint(1, 12))
            order.refresh_from_db()
            order.total_paid = (order.total_amount
                                * Decimal(random.choice(["0.5", "0.75", "1"]))
                                ).quantize(Decimal("0.01"))
            order.save()

        # --- Purchases with 1-4 line items each ---
        for _ in range(Purchase.objects.count(), N):
            purchase = Purchase.objects.create(
                supplier=random.choice(suppliers),
                employee=random.choice(employees),
            )
            for prod in random.sample(products, random.randint(1, 4)):
                PurchaseDetail.objects.create(
                    purchase=purchase, product=prod,
                    quantity=random.randint(5, 40))
            purchase.total_paid = Decimal("0")
            purchase.calculate_totals()
            purchase.total_paid = (purchase.total_amount
                                   * Decimal(random.choice(["0.5", "0.75", "1"]))
                                   ).quantize(Decimal("0.01"))
            purchase.calculate_totals()
            purchase.save()

        self.stdout.write(self.style.SUCCESS(
            "Seed complete -> "
            f"Customers={Customer.objects.count()} "
            f"Suppliers={Supplier.objects.count()} "
            f"Categories={Category.objects.count()} "
            f"Products={Product.objects.count()} "
            f"Employees={Employee.objects.count()} "
            f"Orders={Order.objects.count()} "
            f"Purchases={Purchase.objects.count()}"
        ))
