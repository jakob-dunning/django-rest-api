from django.urls import path
from .views.product import Product

urlpatterns = [
    path('product/', Product.as_view()),
    path('product/<int:product_id>/', Product.as_view()),
]