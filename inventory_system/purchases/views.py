from django.shortcuts import render, redirect, get_object_or_404
from .models import Purchase
from .forms import PurchaseForm, PurchaseDetailFormSet
from employees.decorators import employee_login_required

@employee_login_required
def purchase_list(request):
    purchases = Purchase.objects.select_related('supplier', 'employee').all()
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})

@employee_login_required
def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)

        if form.is_valid():
            purchase = form.save()  # Save to get primary key
            formset = PurchaseDetailFormSet(request.POST, instance=purchase)

            if formset.is_valid():
                details = formset.save(commit=False)
                for item in details:
                    item.total_price = item.product.cost_price * item.quantity
                    item.save()
                formset.save_m2m()

                purchase.calculate_totals()
                purchase.save(update_fields=['total_amount', 'total_remain'])

                return redirect('purchase_list')
        else:
            formset = PurchaseDetailFormSet(request.POST)
    else:
        form = PurchaseForm()
        formset = PurchaseDetailFormSet()

    return render(request, 'purchase/purchase_add.html', {'form': form,'formset': formset})

@employee_login_required
def purchase_detail(request, pk):
    purchase = Purchase.objects.filter(pk=pk).first()
    return render(request, 'purchase/purchase_detail.html', {'purchase': purchase})
