from rest_framework import viewsets, filters


from api.reviews.serializers import ReviewSerializer
from api.reviews.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        return Review.objects.filter(product__public_id=self.kwargs['product_public_id'])

    def get_object(self):
        obj = Review.objects.get_object_by_public_id(self.kwargs['public_id'])

        self.check_object_permissions(self.request, obj)

        return obj

