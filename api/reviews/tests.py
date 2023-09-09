import pytest

from api.fixtures.user import user, admin
from api.fixtures.product import product_factory
from api.reviews.models import Review


@pytest.mark.django_db
def test_create_review(user, product_factory):
    product = product_factory()
    user.products_bought.add(product)
    review = Review.objects.create(author=user, product=product, rating=1, text="test_text")
    assert review.author == user
    assert review.product == product
    assert review.rating == 1
    assert review.text == "test_text"

