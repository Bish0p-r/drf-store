import pytest

from api.products.models import Product, ProductCategory, Brand
from api.reviews.models import Review
from api.user.models import User


@pytest.fixture
def review(db) -> Review:
    user = User.objects.create_user(
        username="test_user_review",
        email="testreview@gmail.com",
        password="test_password_review"
    )
    brand = Brand.objects.create(name="Test Brand")
    category = ProductCategory.objects.create(name="Test Category")
    product = Product.objects.create(name="Test", category=category, price=111)
    product.brands.add(brand)
    return Review.objects.create(author=user, product=product, rating=5, text="Test")
