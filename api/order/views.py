import json

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.abstract.viewsets import AbstractViewSet
from api.order.serializers import OrderSerializer
from api.order.models import Order
from api.cart.models import Cart
from api.payment.services import yookassa_create_order


class OrderViewSet(AbstractViewSet):
    serializer_class = OrderSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(initiator=self.request.user)

    def get_object(self):
        obj = Order.objects.get_object_by_public_id(self.kwargs['public_id'])
        self.check_object_permissions(self.request, obj)
        return obj

    # def create(self, request, *args, **kwargs):
    #
    #     user = self.request.user
    #     cart = Cart.objects.filter(user=user)
    #     return_url = '123'
    #
    #     if not cart.exists():
    #         return Response({"rejection": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     order = Order.objects.create(initiator=user)
    #
    #     confirmation_url = yookassa_create_order(order, return_url)
    #
    #     # cart.delete()
    #
    #     return Response({"confirmation_url": confirmation_url}, status=status.HTTP_200_OK)
