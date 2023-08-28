from rest_framework import routers
from api.user.views import UserViewSet
from api.products.views import ProductViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    *router.urls,
]
