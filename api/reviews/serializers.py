from rest_framework import serializers

from api.reviews.models import Review
from api.abstract.serializers import AbstractSerializer


class ReviewSerializer(AbstractSerializer):
    product_public_id = serializers.ReadOnlyField(source="product.public_id")
    author_public_id = serializers.ReadOnlyField(source="author.public_id")

    class Meta:
        model = Review
        fields = (
            "public_id",
            "author_public_id",
            "product_public_id",
            "rating",
            "text",
        )
