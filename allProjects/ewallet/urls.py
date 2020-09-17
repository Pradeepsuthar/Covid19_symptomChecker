from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='E-Wallet Home Page'),
    path('addMoney/', views.addMoney, name='addMoney'),
    path('transactions/', views.Transactions, name='Transactions Page'),
]