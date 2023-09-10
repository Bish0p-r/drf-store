import pytest
from django.utils.text import slugify

from api.products.models import Product, ProductCategory, Size, Brand


data_category = {
    "name": "test_category"
}


@pytest.fixture
def category(db) -> ProductCategory:
    return ProductCategory.objects.create(**data_category)


data_brand = {
    "name": "test_brand"
}


@pytest.fixture
def brand(db) -> Brand:
    return Brand.objects.create(**data_brand)


@pytest.fixture
def product(db) -> Product:
    category = ProductCategory.objects.create(name="Test Category name")
    brand = Brand.objects.create(name="Test Brand name")
    product = Product.objects.create(
        name="Test Product name",
        price=111,
        category=category
    )
    product.brands.add(brand)
    size = Size.objects.create(product=product, name="test_size", quantity=11)
    return product


@pytest.fixture
def product_factory():
    def create_product(name='Test Product', description='', price=10, image=None, sex='U'):
        category = ProductCategory.objects.create(name='Test Category')
        brand = Brand.objects.create(name='Test Brand')

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            image=image,
            sex=sex,
            category=category
        )
        product.brands.add(brand)
        size = Size.objects.create(product=product, name='test_size', quantity=11)

        return product

    yield create_product


@pytest.fixture
def size_factory():
    def create_size(name='S', quantity=1, product=None):
        size = Size.objects.create(
            name=name,
            quantity=quantity,
            product=product
        )

        return size

    yield create_size
