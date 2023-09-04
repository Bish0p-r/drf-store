from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.reviews.models import Review

from api.abstract.serializers import AbstractSerializer
from api.user.models import User
from api.products.models import Product


class ReviewSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='public_id')
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='public_id')

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")

        elif Review.objects.filter(
                author__public_id=self.context["request"].data['author'],
                product__public_id=self.context["request"].data['product']
        ).exists():
            raise ValidationError("You have already written a review.")

        return value
    #
    # def validate_product(self, value):
    #     if self.instance:
    #         return self.instance.product
    #     return value

    class Meta:
        model = Review
        fields = ('id', 'author', 'product', 'rating', 'text',)
