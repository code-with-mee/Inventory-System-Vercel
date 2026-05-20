from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'age', 'phone', 'address', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }