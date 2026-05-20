from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.create_order, name='order_add'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
]