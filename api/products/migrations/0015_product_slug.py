# Generated by Django 4.2.4 on 2023-09-09 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_products', '0014_remove_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=None, max_length=130),
            preserve_default=False,
        ),
    ]