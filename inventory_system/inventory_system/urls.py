"""
URL configuration for inventory_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from customers import urls as customer_urls
from suppliers import urls as supplier_url
from products import urls as product_urls
from employees import urls as employee_urls
from sales import urls as sale_urls
from purchases import urls as purchase_urls
from dashboard import urls as dashboard_urls
from accounts import urls as account_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("customers/",include(customer_urls)),
    path("suppliers/",include(supplier_url)),
    path("",include(product_urls)),
    path("employees/",include(employee_urls)),
    path("orders/",include(sale_urls)),
    path("purchases/",include(purchase_urls)),
    path("",include(dashboard_urls)),
    path("",include(account_urls)),
]
