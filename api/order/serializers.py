from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from api.abstract.serializers import AbstractSerializer
from api.order.models import Order
from api.user.models import User


class OrderSerializer(AbstractSerializer):
    class Meta:
        model = Order
        exclude = ('initiator',)
