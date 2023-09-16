from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework import status, mixins
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.viewsets import GenericViewSet

from api.user.serializers import UserSerializer, BaseUserSerializer
from api.user.models import User
from api.cart.models import Cart
from api.user.permissions import UserPermission


@extend_schema_view(
    list=extend_schema(summary="Получить список пользователей."),
    retrieve=extend_schema(summary="Получить пользователя по public_id."),
)
class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    http_method_names = ("patch", "get", "post")
    permission_classes = (UserPermission,)
    lookup_field = "public_id"

    def get_serializer_class(self):
        """Получение сериалайзера в зависимости от того кем является пользователь."""
        if self.request.user.is_superuser:
            return UserSerializer
        if self.serializer_class:
            return self.serializer_class
        return BaseUserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(Q(is_superuser=True) | Q(is_active=False))

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs["public_id"])
        # Установка более расширенного сериалайзера если пользователь запрашивает свой профиль.
        if self.request.user == obj:
            self.serializer_class = UserSerializer
        return obj

    @extend_schema(summary="Изменить данные пользователя.", methods=["PATCH"])
    def partial_update(self, request, *args, **kwargs):
        """
        Частичная замена атрибутов пользователя.
        - PATCH /api/user/{public_id}/
        """
        instance = self.get_object()
        self.check_object_permissions(self.request, instance)
        serializer = self.get_serializer_class()(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(summary="Очистить корзину пользователя.", methods=["POST"])
    @action(methods=["post"], detail=True)
    def clean_cart(self, request, *args, **kwargs):
        """
        Очистка корзины товаров пользователя.
        - POST /api/user/{public_id}/clean_cart/
        """
        instance = self.get_object()
        self.check_object_permissions(self.request, instance)
        cart = Cart.objects.filter(user=instance)
        serializer = self.get_serializer_class()(instance)
        cart.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
