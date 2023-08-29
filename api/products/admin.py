from django.contrib import admin

from api.reviews.admin import ReviewInline
from api.products.models import Product, ProductCategory, Brand, Size, Gallery


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1


class SizeInline(admin.TabularInline):
    model = Size
    extra = 1


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    filter_horizontal = ('brands',)
    list_display_links = ('name', 'category')
    search_fields = ('name', 'category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryInline, SizeInline, ReviewInline]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
