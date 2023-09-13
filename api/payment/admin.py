from django.contrib import admin

from api.payment.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active')



# admin.site.register(Coupon)
