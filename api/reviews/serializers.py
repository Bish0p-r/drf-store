from rest_framework import serializers
from api.reviews.models import Review

from api.abstract.serializers import AbstractSerializer
from api.user.models import User
from api.products.models import Product


class ReviewSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='public_id')
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='public_id')

    class Meta:
        model = Review
        fields = ('public_id', 'author', 'product', 'rating', 'text',)
