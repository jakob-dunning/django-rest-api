# Generated by Django 5.1.5 on 2025-02-01 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_user_shopping_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcartposition',
            name='shopping_cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_positions', to='api.shoppingcart'),
        ),
    ]
