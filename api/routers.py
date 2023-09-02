from django.urls import path
from rest_framework_nested import routers
from api.user.views import UserViewSet
from api.products.views import ProductViewSet, SizeViewSet
from api.reviews.views import ReviewViewSet
from api.order.views import OrderViewSet
from api.payment.views import CreatePaymentView, CreatePaymentAcceptanceView

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')

router.register(r'product', ProductViewSet, basename='product')

router.register(r'order', OrderViewSet, basename='order')

size_router = routers.NestedSimpleRouter(router, r'product', lookup='product')
size_router.register(r'size', SizeViewSet, basename='product-size')

review_router = routers.NestedSimpleRouter(router, r'product', lookup='product')
review_router.register(r'review', ReviewViewSet, basename='product-review')


urlpatterns = [
    *router.urls,
    *size_router.urls,
    *review_router.urls,
    path('create_payment', CreatePaymentView.as_view()),
    path('payment_acceptance', CreatePaymentAcceptanceView.as_view()),
]
