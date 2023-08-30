from django.db import models

from api.abstract.models import AbstractModel
from api.user.models import User
from api.products.models import Product, Size


# class Cart(AbstractModel):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='carts')
#
#     def __str__(self):
#         return f'Cart id: {self.public_id}'


class Cart(AbstractModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='carts')
    product_size = models.ForeignKey(to=Size, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)

    def sum(self):
        return self.product_size.product.price * self.quantity

    def __str__(self):
        return f'Cart id: {self.public_id} Product: {self.product_size}'


# class CartTest(AbstractModel):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='cartstests')
#     product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='cartstests')
#     size = models.ForeignKey(to=Size.objects.filter(product=product), on_delete=models.CASCADE, related_name='cartstests')
#     quantity = models.PositiveIntegerField(default=1)
#
#     def sum(self):
#         return self.product.price * self.quantity
