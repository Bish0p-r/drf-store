from rest_framework import serializers
from api.user.models import User
from api.abstract.serializers import AbstractSerializer


class UserSerializer(AbstractSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'bio', 'avatar', 'email', 'is_active',
            'created', 'updated', 'wishlist',
        ]
        read_only_field = ['is_active']
