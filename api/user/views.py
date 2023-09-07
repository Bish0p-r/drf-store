from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q

from api.user.serializers import UserSerializer, BaseUserSerializer
from api.user.models import User
from api.abstract.viewsets import AbstractViewSet
from api.cart.models import Cart
from api.auth.permissions import UserPermission


class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get',)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'public_id'

    def get_serializer_class(self):
        """Получение сериалайзера в зависимости кем является пользователь."""
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
        obj = User.objects.get_object_by_public_id(self.kwargs['public_id'])
        # Установка более расширенного сериалайзера если пользователь запрашивает свой профиль.
        if self.request.user == obj:
            self.serializer_class = UserSerializer
        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        """Метод запроса PATCH, частично заменяющий атрибуты пользователя."""
        instance = self.get_object()
        self.check_object_permissions(self.request, instance)
        serializer = self.get_serializer_class()(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def clean_cart(self, request, *args, **kwargs):
        """Очистка корзины товаров пользователя."""
        user = self.request.user
        cart = Cart.objects.filter(user=user)
        serializer = self.serializer_class(user)
        cart.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
