from rest_framework import viewsets, filters


from api.reviews.serializers import ReviewSerializer
from api.reviews.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        s = self
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

