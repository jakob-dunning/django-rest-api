# Generated by Django 5.1.5 on 2025-02-03 22:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_shoppingcartposition_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcartposition',
            name='product',
        ),
        migrations.AddField(
            model_name='shoppingcartposition',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.product'),
            preserve_default=False,
        ),
    ]
