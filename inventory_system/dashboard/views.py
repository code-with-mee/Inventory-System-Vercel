from django.shortcuts import render
from customers.models import Customer
from products.models import Product, Category
from suppliers.models import Supplier
from sales.models import Order
from purchases.models import Purchase
from employees.decorators import employee_login_required

@employee_login_required
def dashboard_home(request):
    # Count totals
    total_category = Category.objects.count()
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_supplier = Supplier.objects.count()

    # Calculate totals using loops
    total_order_amount = sum(order.total_amount or 0 for order in Order.objects.all())
    total_purchase_amount = sum(purchase.total_amount or 0 for purchase in Purchase.objects.all())

    context = {
        'total_category': total_category,
        'total_product': total_product,
        'total_customer': total_customer,
        'total_supplier': total_supplier,
        'total_order_amount': total_order_amount,
        'total_purchase_amount': total_purchase_amount,
    }

    return render(request, 'dashboard/home.html', context)
