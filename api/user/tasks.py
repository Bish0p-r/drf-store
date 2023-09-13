from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task

from api.cart.models import Cart
from api.user.models import User


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def cart_email_notification():
    users = User.objects.filter(
        receive_email_notifications=True,
        carts__created__lt=timezone.now() - timedelta(hours=12)
    )

    if users.exists():
        for user in users:
            subject = "Напоминание о неоплаченной корзине."
            message = "Мы обратили внимание, что у вас осталась неоплаченная корзина товаров на нашем сайте..."

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )


@shared_task
def cart_clear_36():
    carts = Cart.objects.filter(created__lt=timezone.now() - timedelta(hours=36))
    carts.delete()
