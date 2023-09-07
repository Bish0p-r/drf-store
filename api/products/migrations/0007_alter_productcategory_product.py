# Generated by Django 4.2.4 on 2023-09-07 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_products', '0006_remove_product_category_productcategory_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='api_products.product'),
        ),
    ]
