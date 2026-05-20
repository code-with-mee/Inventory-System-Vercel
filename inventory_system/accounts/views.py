from django.shortcuts import render, redirect
from django.contrib import messages
from employees.models import Employee
from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = Employee.objects.get(username=username)
            if check_password(password, user.password):
                request.session['employee_id'] = user.id
                return redirect('dashboard_home')
            else:
                messages.error(request, "Incorrect password")
        except Employee.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'account/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')
