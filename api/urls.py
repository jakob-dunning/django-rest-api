from django.urls import path

from .views.shopping_cart import ShoppingCart
from .views.product import Product
from .views.shopping_cart_position import ShoppingCartPosition
from .views.user import User

urlpatterns = [
    path('product/', Product.as_view()),
    path('product/<int:product_id>/', Product.as_view()),
    path('user/', User.as_view()),
    path('user/<int:user_id>/', User.as_view()),
    path('shopping-cart/', ShoppingCart.as_view()),
    path('shopping-cart/<int:shopping_cart_id>/', ShoppingCart.as_view()),
    path('shopping-cart-position/', ShoppingCartPosition.as_view()),
    path('shopping-cart-position/<int:shopping_cart_position_id>/', ShoppingCartPosition.as_view()),
]