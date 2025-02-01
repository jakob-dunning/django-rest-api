# Generated by Django 5.1.5 on 2025-01-18 02:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(1)])),
                ('model', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1)])),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)])),
                ('category', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(1)])),
            ],
        ),
    ]
