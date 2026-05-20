from django.db import models
from suppliers.models import Supplier
from employees.models import Employee
from products.models import Product

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_remain = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_totals(self):
        if not self.pk:
            return  # can't calculate without saved Purchase
        total = sum((item.total_price or 0) for item in self.items.all())
        self.total_amount = total
        self.total_remain = self.total_amount - self.total_paid

    def __str__(self):
        return self.supplier.name if self.supplier else "Unknown Supplier"


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.product:
            self.total_price = self.product.selling_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name if self.product else "Unknown Product"
