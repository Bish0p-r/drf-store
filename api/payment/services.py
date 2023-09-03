import uuid

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from yookassa import Configuration, Payment

from api.order.models import Order
from api.user.models import User
from api.products.models import Size


def yookassa_create_order(data):
    Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    user_id = data.get('id')
    return_url = data.get('return_url')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    address = data.get('address')

    user = User.objects.get(public_id=user_id)
    cart_history = {str(i.public_id): i.to_json() for i in user.carts.all()}

    order = Order.objects.create(
        initiator=user, cart_history=cart_history, first_name=first_name, last_name=last_name, address=address
    )

    value = order.total_sum

    payment = Payment.create({
        "amount": {
            "value": f"{value}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url,
        },
        "capture": True,
        "description": f"Заказ №{str(order.public_id)}",
        "metadata": {"order_public_id": str(order.public_id)},
    }, uuid.uuid4())

    user.carts.all().delete()

    return payment.confirmation.confirmation_url


def payment_acceptance(response):
    try:
        order = Order.objects.get(public_id=response['object']['metadata']['order_public_id'])

    except ObjectDoesNotExist:
        return False

    if response['event'] == 'payment.succeeded':
        order.status = 1

        for data in order.cart_history.values():
            product_size_id = data['product']['id']
            product_size_quantity = data['product']['quantity']
            product = Size.objects.get_object_by_public_id(product_size_id)
            product.quantity -= int(product_size_quantity)
            product.save()
        order.save()

    elif response['event'] == 'payment.canceled':
        order.status = 4
        order.save()

    return True
