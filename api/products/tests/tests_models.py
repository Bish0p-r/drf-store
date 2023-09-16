import pytest

from django.test import TestCase

from api.fixtures.product import category, brand
from api.products.models import Product


@pytest.mark.django_db
def test_create_product(category, brand):
    product = Product.objects.create(name="test_name", price=111, category=category)
    product.brands.add(brand)
    assert product.price == 111
    assert product.name == "test_name"
    assert product.brands.filter(name=brand.name).exists()
    assert product.category == category
