import pytest

from api.fixtures.user import user, admin, user_variation
from api.fixtures.product import product_factory
from api.fixtures.reviews import review


class TestReviewViewSet:
    base_endpoint = "/api/product/"

    def test_list(self, client, user, admin, product_factory):
        product = product_factory()
        response = client.get(f"{self.base_endpoint}{product.public_id}/review/")
        assert response.status_code == 200

    def test_retrieve(self, client, admin, review):
        product = review.product
        user = review.author
        client.force_authenticate(user=user)
        response = client.get(f"{self.base_endpoint}{product.public_id}/review/{review.public_id}/")
        assert response.status_code == 200
        assert response.data["public_id"] == str(review.public_id)

    def test_create(self, client, user, admin, product_factory):
        product = product_factory()
        client.force_authenticate(user=user)
        response = client.post(f"{self.base_endpoint}{product.public_id}/review/", data={"rating": 5, "text": "Test"})
        assert response.status_code == 403
        user.products_bought.add(product)
        response = client.post(f"{self.base_endpoint}{product.public_id}/review/", data={"rating": 5, "text": "Test"})
        assert response.status_code == 201
        assert response.data["rating"] == 5
        assert response.data["text"] == "Test"
        client.force_authenticate(user=admin)
        response = client.post(f"{self.base_endpoint}{product.public_id}/review/",
                               data={"rating": 3, "text": "Test_admin"})
        assert response.status_code == 201
        assert response.data["rating"] == 3
        assert response.data["text"] == "Test_admin"
        response = client.get(f"{self.base_endpoint}{product.public_id}/review/")
        assert response.status_code == 200
        assert response.data["count"] == 2

    def test_delete(self, client, user, admin, review):
        product = review.product
        client.force_authenticate(user=user)
        response = client.delete(f"{self.base_endpoint}{product.public_id}/review/{review.public_id}/")
        assert response.status_code == 403
        client.force_authenticate(user=review.author)
        response = client.delete(f"{self.base_endpoint}{product.public_id}/review/{review.public_id}/")
        assert response.status_code == 204
