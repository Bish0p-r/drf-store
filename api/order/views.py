import json

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.abstract.viewsets import AbstractViewSet
from api.order.serializers import OrderSerializer
from api.order.models import Order
from api.cart.models import Cart
from api.payment.services import yookassa_create_order


class OrderViewSet(AbstractViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get',)
    lookup_field = 'public_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(initiator=self.request.user)

    def get_object(self):
        obj = Order.objects.get_object_by_public_id(self.kwargs['public_id'])
        self.check_object_permissions(self.request, obj)
        return obj
