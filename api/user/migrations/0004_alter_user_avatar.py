# Generated by Django 4.2.4 on 2023-09-09 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_user', '0003_user_products_bought'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars'),
        ),
    ]