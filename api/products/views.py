from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.abstract.viewsets import AbstractViewSet
from api.products.models import Product, Size
from api.products.serializers import ProductSerializer, SizeSerializer
from api.cart.models import Cart


class ProductViewSet(AbstractViewSet):
    serializer_class = ProductSerializer
    ordering_fields = ['created']
    ordering = ['-created']
    lookup_field = 'public_id'
    http_method_names = ('get', 'post')

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        obj = Product.objects.get_object_by_public_id(self.kwargs['public_id'])

        return obj

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_to_wishlist(self, request, *args, **kwargs):
        product = self.get_object()
        user = self.request.user

        user.add_to_wishlist(product)

        serializer = self.serializer_class(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def remove_from_wishlist(self, request, *args, **kwargs):
        product = self.get_object()
        user = self.request.user

        user.remove_from_wishlist(product)

        serializer = self.serializer_class(product)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SizeViewSet(AbstractViewSet):
    serializer_class = SizeSerializer
    filter_backends = [filters.OrderingFilter]
    lookup_field = 'public_id'
    http_method_names = ('get', 'post',)

    def get_queryset(self):
        return Size.objects.filter(product__public_id=self.kwargs['product_public_id'])

    def get_object(self):
        obj = Size.objects.get_object_by_public_id(self.kwargs['public_id'])

        self.check_object_permissions(self.request, obj)

        return obj

    @action(methods=['post'], detail=True,  permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, *args, **kwargs):
        size = self.get_object()
        user = self.request.user
        quantity = int(request.data.get('quantity') or 1)

        cart = Cart.objects.filter(user=user, product_size=size)

        if cart.exists():
            cart = cart.first()
            if cart.quantity + quantity >= size.quantity:
                cart.quantity = size.quantity
            else:
                cart.quantity += quantity
        else:
            cart = Cart.objects.create(user=user, product_size=size, quantity=min(size.quantity, quantity))

        cart.save()
        serializer = self.serializer_class(size)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def remove_from_cart(self, request, *args, **kwargs):
        size = self.get_object()
        user = self.request.user
        quantity = int(request.data.get('quantity') or 1)

        cart = Cart.objects.filter(user=user, product_size=size)

        if cart.exists():
            cart = cart.first()
            if cart.quantity - quantity <= 0:
                cart.delete()
            else:
                cart.quantity -= quantity
                cart.save()

        serializer = self.serializer_class(size)

        return Response(serializer.data, status=status.HTTP_200_OK)
