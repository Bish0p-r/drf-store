from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.reviews.models import Review

from api.abstract.serializers import AbstractSerializer
from api.user.models import User
from api.products.models import Product


class ReviewSerializer(AbstractSerializer):
    product_public_id = serializers.ReadOnlyField(source='product.public_id')
    author_public_id = serializers.ReadOnlyField(source='author.public_id')

    class Meta:
        model = Review
        fields = ('id', 'author_public_id', 'product_public_id', 'rating', 'text')
