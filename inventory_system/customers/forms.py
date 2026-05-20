from django import forms
from .models import Customer

class CustomerAddForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields =["name","phone","address"]

class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields =["name","phone","address"]