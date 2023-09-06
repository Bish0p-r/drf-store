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
        """Валидация пользователя по публичному идентификатору."""
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")
        # Проверка писал ли пользователь отзыв для этого товара.
        elif self.context["request"].method == 'POST' and Review.objects.filter(
                author__public_id=self.context["request"].data['author'],
                product__public_id=self.context["request"].data['product']
        ).exists():
            raise ValidationError("You have already written a review.")

        return value

    def validate_product(self, value):
        """Валидация продукта по публичному идентификатору продукта в теле запроса и URL запроса."""
        request = self.context['request']
        if request.data['product'] != request.parser_context['kwargs']['product_public_id']:
            raise ValidationError("You can't create a review for another product.")
        return value

    class Meta:
        model = Review
        fields = ('id', 'author', 'product', 'rating', 'text',)
