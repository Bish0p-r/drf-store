# Generated by Django 4.2.4 on 2023-09-09 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_products', '0020_brand_slug_product_slug_productcategory_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='slug',
        ),
    ]
