# Generated by Django 5.1.5 on 2025-02-01 17:15

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)])),
                ('shopping_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.shoppingcart')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50, validators=[django.core.validators.EmailValidator()])),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(1)])),
                ('shopping_cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.shoppingcart')),
            ],
        ),
    ]
