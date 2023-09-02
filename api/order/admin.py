from django.contrib import admin

from api.order.models import Order


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1
    