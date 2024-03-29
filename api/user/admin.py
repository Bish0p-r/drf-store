from django.contrib import admin
from api.user.models import User
from api.reviews.admin import ReviewInline
from api.cart.admin import CartInline
from api.order.admin import OrderInline


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
    )
    filter_horizontal = ("wishlist",)
    inlines = (ReviewInline, CartInline, OrderInline)
    fields = (
        "username",
        "email",
        "password",
        "last_login",
        "first_name",
        "last_name",
        "bio",
        "avatar",
        "is_active",
        "is_superuser",
        "wishlist",
    )
