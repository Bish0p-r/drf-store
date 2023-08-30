from rest_framework import serializers
from api.user.models import User
from api.abstract.serializers import AbstractSerializer
from api.cart.serializers import CartSerializer


class UserSerializer(AbstractSerializer):
    id = serializers.UUIDField(source='public_id', format='hex')
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    carts = CartSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'bio', 'avatar', 'email', 'is_active',
            'created', 'updated', 'wishlist', 'carts'
        ]
        read_only_field = ['is_active']
