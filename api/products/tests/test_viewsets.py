import pytest

from rest_framework import status

from api.fixtures.product import product_factory, product
from api.fixtures.user import user, admin
from api.products.models import Product, ProductCategory, Brand, Size
from api.user.models import User


class TestProductSizeViewSet:
    endpoint = '/api/product/'

    def test_list(self, client, user, product_factory):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        product = product_factory()
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_retrieve(self, client, user, product_factory):
        client.force_authenticate(user=user)
        product = product_factory()
        response = client.get(f"{self.endpoint}{product.public_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['public_id'] == str(product.public_id)

    def test_add_to_wishlist(self, client, user, product_factory):
        client.force_authenticate(user=user)
        product = product_factory()
        response = client.post(f"{self.endpoint}{product.public_id}/add_to_wishlist/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['public_id'] == str(product.public_id)
        assert user.wishlist.filter(public_id=product.public_id).exists()

    def test_remove_from_wishlist(self, client, user, product_factory):
        client.force_authenticate(user=user)
        product1 = product_factory()
        product2 = product_factory()
        user.wishlist.add(product1)
        user.wishlist.add(product2)
        response = client.post(f"{self.endpoint}{product1.public_id}/remove_from_wishlist/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['public_id'] == str(product1.public_id)
        assert not user.wishlist.filter(public_id=product1.public_id).exists()
        assert user.wishlist.filter(public_id=product2.public_id).exists()

    def test_unauthorized(self, client, user, product_factory):
        product1 = product_factory()
        response = client.post(f"{self.endpoint}{product1.public_id}/remove_from_wishlist/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_size_list(self, client, user, product_factory):
        product = product_factory()
        response = client.get(f"{self.endpoint}{product.public_id}/size/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_size_retrieve(self, client, user, product_factory):
        product = product_factory()
        size = product.sizes.first()
        response = client.get(f"{self.endpoint}{product.public_id}/size/{size.public_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["public_id"] == str(size.public_id)

    def test_add_or_remove_cart(self, client, user, product_factory):
        product = product_factory()
        size = product.sizes.first()
        response = client.post(f"{self.endpoint}{product.public_id}/size/{size.public_id}/add_to_cart/",)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        client.force_authenticate(user=user)
        response = client.post(f"{self.endpoint}{product.public_id}/size/{size.public_id}/add_to_cart/",
                               data={"quantity": 3})
        assert response.status_code == status.HTTP_200_OK
        assert user.carts.filter(product_size=size, quantity=3).exists()
        response = client.post(f"{self.endpoint}{product.public_id}/size/{size.public_id}/remove_from_cart/",
                               data={"quantity": 2})
        assert response.status_code == status.HTTP_200_OK
        assert user.carts.filter(product_size=size, quantity=1).exists()
        response = client.post(f"{self.endpoint}{product.public_id}/size/{size.public_id}/remove_from_cart/",
                               data={"quantity": 3})
        assert response.status_code == status.HTTP_200_OK
        assert not user.carts.filter(product_size=size).exists()
