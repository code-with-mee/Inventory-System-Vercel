from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchase_list, name='purchase_list'),
    path('add/', views.create_purchase, name='purchase_add'),
    path('<int:pk>/', views.purchase_detail, name='purchase_detail'),
]