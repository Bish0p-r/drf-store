from django.db import models

from api.user.models import User
from api.abstract.models import AbstractModel


class Order(AbstractModel):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    CANCELLED = 4
    STATUSES = (
        (CREATED, "Создан"),
        (PAID, "Оплачен"),
        (ON_WAY, "В пути"),
        (DELIVERED, "Доставлен"),
        (CANCELLED, "Отменен"),
    )

    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=255, blank=True)
    cart_history = models.JSONField(default=dict)
    status = models.IntegerField(choices=STATUSES, default=CREATED)

    initiator = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="orders"
    )

    def already_delivered(self, product_id):
        return (
            self.status == Order.DELIVERED
            and self.cart_history["product"]["product_id"] == product_id
        )

    @property
    def total_sum(self):
        return sum(i.sum() for i in self.initiator.carts.all())

    def __str__(self):
        return f"Order #{self.public_id} from {self.initiator.email}"
