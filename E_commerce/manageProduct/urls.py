from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_all_products),
    path('products/<int:pk>/', views.get_product),
    path('products/create/', views.create_product),
    path('products/update/<int:pk>/', views.update_product),
    path('products/delete/<int:pk>/', views.delete_product),
]