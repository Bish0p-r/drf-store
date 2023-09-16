import pytest
from api.user.models import User


data_user = {
    "username": "test_user",
    "email": "test@gmail.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "test_password",
}

data_user_variation = {
    "username": "test_user_variation",
    "email": "testvariation@gmail.com",
    "first_name": "Test_variation",
    "last_name": "User_variation",
    "password": "test_password_variation",
}

data_superuser = {
    "username": "test_superuser",
    "email": "testsuperuser@gmail.com",
    "first_name": "Test",
    "last_name": "Superuser",
    "password": "test_password",
}


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(**data_user)


@pytest.fixture
def user_variation(db) -> User:
    return User.objects.create_user(**data_user_variation)


@pytest.fixture
def admin(db) -> User:
    return User.objects.create_superuser(**data_superuser)
