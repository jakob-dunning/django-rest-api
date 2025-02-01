from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, EmailValidator
from django.db import models


class Product(models.Model):
    manufacturer = models.CharField(max_length=30, validators=[MinLengthValidator(1)])
    model = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    category = models.CharField(max_length=30, validators=[MinLengthValidator(1)])


class ShoppingCart(models.Model):
    pass


class ShoppingCartPosition(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)])


class User(models.Model):
    email = models.CharField(max_length=50, validators=[EmailValidator()])
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)])
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)
