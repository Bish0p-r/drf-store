# Generated by Django 4.2.4 on 2023-09-09 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_products', '0015_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]