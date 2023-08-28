from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.products.models import Product
from api.products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created']
    ordering = ['-created']

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        obj = Product.objects.get(pk=self.kwargs['pk'])

        self.check_object_permissions(self.request, obj)

        return obj

    @action(methods=['post'], detail=True)
    def add_to_wishlist(self, request, *args, **kwargs):
        product = self.get_object()
        user = self.request.user

        user.add_to_wishlist(product)

        serializer = self.serializer_class(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def remove_from_wishlist(self, request, *args, **kwargs):
        product = self.get_object()
        user = self.request.user

        user.remove_from_wishlist(product)

        serializer = self.serializer_class(product)

        return Response(serializer.data, status=status.HTTP_200_OK)
