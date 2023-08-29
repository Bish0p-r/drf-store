from rest_framework import viewsets, filters


from api.reviews.serializers import ReviewSerializer
from api.reviews.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # return Review.objects.get_object_by_public_id(self.kwargs['product_pk'])
       return Review.objects.filter(product__public_id=self.kwargs['product_pk'])

    def get_object(self):
        obj = Review.objects.get_object_by_public_id(self.kwargs['pk'])

        self.check_object_permissions(self.request, obj)

        return obj

