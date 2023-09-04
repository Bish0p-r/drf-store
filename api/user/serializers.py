from rest_framework import serializers

from api.user.models import User
from api.abstract.serializers import AbstractSerializer
from api.cart.serializers import CartSerializer
from api.order.serializers import OrderSerializer


class UserSerializer(AbstractSerializer):
    carts = CartSerializer(many=True)
    orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'bio', 'avatar', 'email', 'is_active', 'created',
            'updated', 'wishlist', 'carts', 'orders',
        )
        read_only_field = (
            'is_active', 'created', 'updated', 'wishlist',
            'carts', 'orders', 'id', 'username', 'email',
        )


class BaseUserSerializer(AbstractSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'bio', 'avatar', 'created',
        )
