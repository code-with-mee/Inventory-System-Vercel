from django import forms
from django.forms import inlineformset_factory
from .models import Purchase, PurchaseDetail
from products.models import Product

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'total_amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'total_remain': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'created_at': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
        }

class PurchaseDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetail
        fields = ['product', 'quantity']

PurchaseDetailFormSet = inlineformset_factory(
    Purchase,
    PurchaseDetail,
    form=PurchaseDetailForm,
    extra=3,
)
