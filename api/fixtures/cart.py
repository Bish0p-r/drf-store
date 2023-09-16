import pytest

from api.cart.models import Cart
from api.user.models import User
from api.products.models import Product, Size, ProductCategory, Brand
from api.fixtures.product import product


@pytest.fixture
def cart(db) -> Cart:
    user = User.objects.create_user(
        username="test_user_cart",
        email="test_cart@gmail.com",
        first_name="Test_cart",
        last_name="User_cart",
        password="test_password",
    )
    category = ProductCategory.objects.create(name="Test Category name")
    brand = Brand.objects.create(name="Test Brand name")
    product = Product.objects.create(
        name="Test Product name", price=111, category=category
    )
    product.brands.add(brand)
    size = Size.objects.create(product=product, name="test_size", quantity=11)
    return Cart.objects.create(user=user, product_size=size)
