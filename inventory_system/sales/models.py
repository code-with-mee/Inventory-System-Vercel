from django.db import models
from employees.models import Employee
from customers.models import Customer
from products.models import Product

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_remain = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_totals(self):
        total = 0
        for item in self.items.all():
            total += item.total_price or 0
        self.total_amount = total
        self.total_remain = self.total_amount - self.total_paid


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if not is_new:
            self.calculate_totals()
            super().save(update_fields=['total_amount', 'total_remain'])

    def __str__(self):
        return self.customer.name


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.product:
            self.total_price = self.product.selling_price * self.quantity
        super().save(*args, **kwargs)
        if self.order:
            self.order.save()


    def __str__(self):
        return self.product.name