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


# data_product = {
#     "name": "test_product",
#     "price": 111,
#     "category": category,
# }


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
    return product


data_size = {
    "name": "test_product",
    "quantity": 11,
    "product": product
}


@pytest.fixture
def size(db) -> Size:
    return Size.objects.create(**data_size)


@pytest.fixture
def product_factory():
    def create_product(name='Test Product', description='', price=10, image=None, sex='U'):
        category = ProductCategory.objects.create(name='Test Category')
        brand = Brand.objects.create(name='Test Brand')
        # category_slug = slugify('Test Category')
        #
        # while ProductCategory.objects.filter(slug=category_slug).exists():
        #     category_slug += 'asd'
        #
        # category = ProductCategory.objects.create(name='Test Category', slug=category_slug)
        #
        # brand_slug = slugify('Test Brand')
        #
        # while Brand.objects.filter(slug=brand_slug).exists():
        #     brand_slug += 'asd'
        #
        # brand = Brand.objects.create(name='Test Brand', slug=brand_slug)
        #
        # unique_slug = slugify('Test Product')
        #
        # while Product.objects.filter(slug=unique_slug).exists():
        #     unique_slug += 'asd'

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            image=image,
            # slug=unique_slug,
            sex=sex,
            category=category
        )
        product.brands.add(brand)

        return product

    yield create_product
