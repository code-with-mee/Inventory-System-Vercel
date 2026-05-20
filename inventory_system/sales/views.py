from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .forms import OrderForm, OrderDetailFormSet
from employees.decorators import employee_login_required

@employee_login_required
def order_list(request):
    orders = Order.objects.select_related('customer', 'employee').all()
    return render(request, 'sale/order_list.html', {'orders': orders})

@employee_login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save()  # Must be saved to get a primary key
            formset = OrderDetailFormSet(request.POST, instance=order)

            if formset.is_valid():
                details = formset.save(commit=False)
                for item in details:
                    item.total_price = item.product.selling_price * item.quantity
                    item.save()
                formset.save_m2m()
                order.save()
                return redirect('order_list')
        else:
            # Use empty formset (not bound to unsaved order) only if form is invalid
            formset = OrderDetailFormSet()

    else:
        form = OrderForm()
        formset = OrderDetailFormSet()

    return render(request, "sale/order_add.html", {
        'form': form,
        'formset': formset
    })

@employee_login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'sale/order_detail.html', {'order': order})
