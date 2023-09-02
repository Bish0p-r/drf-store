from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.user.serializers import UserSerializer
from api.user.models import User
from api.abstract.viewsets import AbstractViewSet
from api.cart.models import Cart
from api.order.models import Order


class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get', 'post',)
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        ip = self.request.META['REMOTE_ADDR']
        print(ip)
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['public_id'])
        self.check_object_permissions(self.request, obj)
        return obj

    @action(methods=['post'], detail=True)
    def clean_cart(self, request, *args, **kwargs):
        user = self.request.user
        cart = Cart.objects.filter(user=user)

        cart.delete()

        serializer = self.serializer_class(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

















    # @action(methods=['post'], detail=True)
    # def order_create(self, request, *args, **kwargs):
    #     user = self.request.user
    #     cart = Cart.objects.filter(user=user)
    #
    #     if not cart.exists():
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     order = Order.objects.create(user=user)
    #
    #
    #     serializer = self.serializer_class(user)
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)
