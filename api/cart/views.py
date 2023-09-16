from api.cart.serializers import CartSerializer
from api.abstract.viewsets import AbstractViewSet


class CartViewSet(AbstractViewSet):
    serializer_class = CartSerializer
