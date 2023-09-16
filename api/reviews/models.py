from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.user.models import User
from api.products.models import Product
from api.abstract.models import AbstractModel


class Review(AbstractModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", editable=False
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews", editable=False
    )

    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(max_length=512, blank=True)
    edited = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"{self.author} - {self.product}"
