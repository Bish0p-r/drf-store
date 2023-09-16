from rest_framework import serializers

from api.cart.models import Cart
from api.abstract.serializers import AbstractSerializer
from api.products.serializers import SizeSerializer


class CartSerializer(AbstractSerializer):
    product_size = SizeSerializer()
    quantity = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = (
            "public_id",
            "product_size",
            "quantity",
        )


class CartHistorySerializer(AbstractSerializer):
    product_size = SizeSerializer()

    class Meta:
        model = Cart
        fields = "__all__"
