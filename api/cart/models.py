from django.db import models

from api.abstract.models import AbstractModel
from api.user.models import User
from api.products.models import Size


class Cart(AbstractModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="carts")
    product_size = models.ForeignKey(
        to=Size, on_delete=models.CASCADE, related_name="carts"
    )

    quantity = models.PositiveIntegerField(default=1)

    def sum(self):
        return self.product_size.product.price * self.quantity

    def to_json(self):
        data = {
            "total_price": float(self.sum()),
            "product": {
                "product_id": str(self.product_size.product.public_id),
                "size_id": str(self.product_size.public_id),
                "name": self.product_size.product.name,
                "size": self.product_size.name,
                "quantity": float(self.quantity),
                "price": float(self.product_size.product.price),
            },
        }

        return data

    def __str__(self):
        return f"Cart id: {self.public_id} Product: {self.product_size}"
