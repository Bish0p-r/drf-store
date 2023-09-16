# Generated by Django 4.2.4 on 2023-09-15 09:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("api_products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "public_id",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "username",
                    models.CharField(db_index=True, max_length=255, unique=True),
                ),
                ("first_name", models.CharField(blank=True, max_length=255)),
                ("last_name", models.CharField(blank=True, max_length=255)),
                (
                    "email",
                    models.EmailField(db_index=True, max_length=254, unique=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_superuser", models.BooleanField(default=False)),
                ("receive_email_notifications", models.BooleanField(default=True)),
                ("bio", models.TextField(blank=True, null=True)),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="avatars"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "products_bought",
                    models.ManyToManyField(
                        blank=True,
                        related_name="products_bought_by",
                        to="api_products.product",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "wishlist",
                    models.ManyToManyField(
                        blank=True,
                        related_name="wishlist_by",
                        to="api_products.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]