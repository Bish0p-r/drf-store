from django.core.validators import MaxValueValidator
from django.db import models
from api.abstract.models import AbstractModel


class Coupon(AbstractModel):
    """Модель купона на скидку."""
    code = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    expired_at = models.DateTimeField(blank=True, null=True)
    amount_discount = models.DecimalField(max_digits=2, decimal_places=0, validators=[MaxValueValidator(99)])

    def __str__(self):
        return self.code
