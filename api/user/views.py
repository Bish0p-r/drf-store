from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from api.user.serializers import UserSerializer
from api.user.models import User
from api.abstract.viewsets import AbstractViewSet


class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get')
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['public_id'])
        self.check_object_permissions(self.request, obj)
        return obj
