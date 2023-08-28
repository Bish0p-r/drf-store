from django.contrib import admin
from api.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',)
    filter_horizontal = ('wishlist',)
