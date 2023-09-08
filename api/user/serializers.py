from rest_framework import serializers

from api.user.models import User
from api.abstract.serializers import AbstractSerializer
from api.cart.serializers import CartSerializer
from api.order.serializers import OrderSerializer
from api.reviews.serializers import ReviewSerializer


class UserSerializer(AbstractSerializer):
    carts = CartSerializer(many=True)
    orders = OrderSerializer(many=True)
    wishlist = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'bio', 'avatar', 'email', 'is_active', 'created',
            'updated', 'wishlist', 'carts', 'orders', 'reviews',
        )
        read_only_field = (
            'is_active', 'created', 'updated', 'wishlist', 'id',
            'carts', 'orders', 'reviews', 'username', 'email',
        )


class BaseUserSerializer(AbstractSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'bio', 'avatar', 'created',
        )
