from django.urls import path

from . import views

app_name = "pharmacists"

urlpatterns = [
    path('', views.list_pharmacists, name='pharmacist-list'),
    path('inventory/', views.inventory_list, name='inventory-list'),
    path('inventory/add/', views.inventory_create, name='inventory-add'),
    path('inventory/<int:pk>/edit/', views.inventory_update, name='inventory-edit'),
]

