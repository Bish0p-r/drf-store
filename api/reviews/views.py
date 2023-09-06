
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from api.reviews.serializers import ReviewSerializer
from api.reviews.models import Review
from api.auth.permissions import UserPermission
from api.products.models import Product


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (UserPermission,)

    lookup_field = 'public_id'

    def get_queryset(self):
        return Review.objects.filter(product__public_id=self.kwargs['product_public_id'])

    def get_object(self):
        return Review.objects.get_object_by_public_id(self.kwargs['public_id'])

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

