import pytest

from api.fixtures.user import user, admin, user_variation
from api.fixtures.product import product_factory
from api.fixtures.cart import cart


class TestUserViewSet:
    endpoint = "/api/user/"

    def test_list(self, client, user, admin):
        response = client.get("/api/user/")
        assert response.status_code == 401
        client.force_authenticate(user=user)
        response = client.get("/api/user/")
        assert response.status_code == 200
        assert response.data["count"] == 1
        client.force_authenticate(user=admin)
        response = client.get("/api/user/")
        assert response.status_code == 200
        assert response.data["count"] == 2

    def test_retrieve(self, client, user, admin, user_variation):
        response = client.get(f"/api/user/{user.public_id}/")
        assert response.status_code == 401
        client.force_authenticate(user=user)
        response = client.get(f"/api/user/{user.public_id}/")
        assert response.status_code == 200
        assert response.data["public_id"] == str(user.public_id)
        assert "carts" in response.data.keys()
        client.force_authenticate(user=user_variation)
        response = client.get(f"/api/user/{user.public_id}/")
        assert response.status_code == 200
        assert "carts" not in response.data.keys()

    def test_partial_update(self, client, user, admin, user_variation):
        client.force_authenticate(user=user)
        response = client.patch(
            f"/api/user/{user.public_id}/",
            {"is_active": False, "first_name": "Test_Name"},
        )
        assert response.status_code == 200
        assert response.data["is_active"] == True
        assert response.data["first_name"] == "Test_Name"
        client.force_authenticate(user=user_variation)
        response = client.patch(
            f"/api/user/{user.public_id}/",
            {"is_active": False, "first_name": "Test_permission"},
        )
        assert response.status_code == 403
        client.force_authenticate(user=admin)
        response = client.patch(
            f"/api/user/{user.public_id}/",
            {"is_active": False, "first_name": "Test_admin_permission"},
        )
        assert response.status_code == 200
        assert response.data["first_name"] == "Test_admin_permission"

    def test_clean_cart(self, client, admin, user_variation, cart):
        user = cart.user
        client.force_authenticate(user=user)
        assert user.carts.count() == 1
        response = client.post(f"/api/user/{user.public_id}/clean_cart/")
        assert response.status_code == 200
        assert user.carts.count() == 0
        client.force_authenticate(user=user_variation)
        response = client.post(f"/api/user/{user.public_id}/clean_cart/")
        assert response.status_code == 403
        client.force_authenticate(user=admin)
        response = client.post(f"/api/user/{user.public_id}/clean_cart/")
        assert response.status_code == 200
