from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path('', views.payment_list, name='payment-list'),
    path('<int:pk>/pay/', views.payment_checkout, name='payment-checkout'),
    path('<int:pk>/receipt/', views.payment_receipt, name='payment-receipt'),
    path('<int:pk>/refund/', views.payment_refund, name='payment-refund'),
]

