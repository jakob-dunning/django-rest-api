from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


class Product(models.Model):
    manufacturer = models.CharField(max_length=30, validators=[MinLengthValidator(1)])
    model = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    category = models.CharField(max_length=30, validators=[MinLengthValidator(1)])
