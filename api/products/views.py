from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.products.models import Product, Size
from api.products.serializers import ProductSerializer, SizeSerializer
from api.cart.models import Cart


@extend_schema_view(
    list=extend_schema(summary="Получить список товаров."),
    retrieve=extend_schema(summary="Получить товар по public_id.")
)
class ProductViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created"]
    ordering = ["-created"]
    lookup_field = "public_id"
    http_method_names = ("get", "post", "options")

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        obj = Product.objects.get_object_by_public_id(self.kwargs["public_id"])
        return obj

    @extend_schema(summary="Добавить продукт в список желаний.", methods=["POST"])
    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def add_to_wishlist(self, request, *args, **kwargs):
        """
        - POST /api/product/{public_id}/add_to_wishlist/
        """
        product = self.get_object()
        user = self.request.user

        user.add_to_wishlist(product)

        serializer = self.serializer_class(product)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="Удалить продукт из списка желаний.", methods=["POST"])
    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def remove_from_wishlist(self, request, *args, **kwargs):
        """
        Удаление продукта из списка желаний.
        - POST /api/product/{public_id}/remove_from_wishlist/
        """
        product = self.get_object()
        user = self.request.user

        user.remove_from_wishlist(product)

        serializer = self.serializer_class(product)

        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(summary="Получить список размеров товара."),
    retrieve=extend_schema(summary="Получить размер товар по public_id.")
)
class SizeViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    serializer_class = SizeSerializer
    filter_backends = [filters.OrderingFilter]
    lookup_field = "public_id"
    http_method_names = ("get", "post", "options")

    def get_queryset(self):
        return Size.objects.filter(product__public_id=self.kwargs["product_public_id"])

    def get_object(self):
        obj = Size.objects.get_object_by_public_id(self.kwargs["public_id"])

        self.check_object_permissions(self.request, obj)

        return obj

    @extend_schema(summary="Добавить продукт в корзину.", methods=["POST"])
    @action(methods=["post"], detail=True,  permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, *args, **kwargs):
        """
        Создание корзины и добавление экземпляра продукта в корзину
        или увеличение количества если товар уже есть в корзине.
        - POST /api/product/{product_public_id}/size/{public_id}/add_to_cart/
        """
        size = self.get_object()
        user = self.request.user
        quantity = int(request.data.get("quantity") or 1)

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

    @extend_schema(summary="Удалить продукт из корзины.", methods=["POST"])
    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def remove_from_cart(self, request, *args, **kwargs):
        """
        Уменьшение на определенное количество экземпляров продукта или удаление полностью из корзины.
        - POST /api/product/{product_public_id}/size/{public_id}/remove_from_cart/
        """
        size = self.get_object()
        user = self.request.user
        quantity = int(request.data.get("quantity") or 1)

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
