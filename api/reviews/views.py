from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.reviews.serializers import ReviewSerializer
from api.reviews.models import Review
from api.auth.permissions import UserPermission
from api.products.models import Product


@extend_schema_view(
    list=extend_schema(summary="Получить список отзывов на товар."),
    retrieve=extend_schema(summary="Получить отзыв по public_id."),
    destroy=extend_schema(summary="Удалить отзыв по public_id."),
)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (UserPermission,)
    http_method_names = ('post', 'get', 'patch', 'delete',)
    lookup_field = 'public_id'

    def get_queryset(self):
        return Review.objects.filter(product__public_id=self.kwargs['product_public_id'])

    def get_object(self):
        obj = Review.objects.get_object_by_public_id(self.kwargs['public_id'])
        return obj

    @extend_schema(summary='Добавить отзыв на купленный товар.', methods=["POST"])
    def create(self, request, *args, **kwargs):
        """
        Создание отзыва на товар при условие что пользователь уже купил его.
        - POST /api/product/{public_id}/review/
        """
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(summary='Изменить отзыв.', methods=["PATCH"])
    def partial_update(self, request, *args, **kwargs):
        """
        Частичная замена атрибутов отзыва.
        - PATCH /api/product/{product_public_id}/review/{public_id}/
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        self.check_object_permissions(self.request, instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Метод проверяющий писал ли пользователь отзыв на товар или нет,
        после чего присваивает модель пользователя и товара к модели отзыва и сохраняет ее.
        """
        product = Product.objects.get_object_by_public_id(self.kwargs['product_public_id'])
        self.check_object_permissions(self.request, product)

        # Проверка писал ли пользователь отзыв для этого товара.
        if not self.request.user.is_superuser and Review.objects.filter(
                author=self.request.user, product=product).exists():
            raise ValidationError("You have already written a review for this product.")

        serializer.save(author=self.request.user, product=product)


