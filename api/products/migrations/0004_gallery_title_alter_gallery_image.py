# Generated by Django 4.2.4 on 2023-09-07 12:47

from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api_products', '0003_size_created_size_public_id_size_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='title',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='gallery'),
        ),
    ]
