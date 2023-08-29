from rest_framework_nested import routers
from api.user.views import UserViewSet
from api.products.views import ProductViewSet, SizeViewSet
from api.reviews.views import ReviewViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'product', ProductViewSet, basename='product')

size_router = routers.NestedSimpleRouter(router, r'product', lookup='product')
size_router.register(r'size', SizeViewSet, basename='product-size')

review_router = routers.NestedSimpleRouter(router, r'product', lookup='product')
review_router.register(r'review', ReviewViewSet, basename='product-review')


urlpatterns = [
    *router.urls,
    *size_router.urls,
    *review_router.urls,
]
