from django.contrib import admin
from api.reviews.models import Review


class ReviewInline(admin.TabularInline):
    extra = 1
    model = Review
