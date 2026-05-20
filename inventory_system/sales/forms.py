from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderDetail

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'total_amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'total_remain': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'created_at': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
        }

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity']

OrderDetailFormSet = inlineformset_factory(
    Order,
    OrderDetail,
    form=OrderDetailForm,
    extra=3
)