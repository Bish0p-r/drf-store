from api.abstract.serializers import AbstractSerializer
from api.order.models import Order


class OrderSerializer(AbstractSerializer):
    class Meta:
        model = Order
        exclude = ("initiator",)
