from django.contrib import admin

from api.cart.models import Cart


class CartInline(admin.TabularInline):
    model = Cart
    extra = 1
