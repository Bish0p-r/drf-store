from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from api.payment.models import Coupon


@shared_task
def send_order_status_notification(email, order_id, status):
    subject = f"Изменение статуса вашего заказа №{order_id}"
    message = f"Ваш заказ №{order_id} был отменен."

    if status == 'payment.succeeded':
        message = f"Ваш заказ №{order_id} был успешно оплачен."

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


@shared_task
def coupon_deactivation():
    expired_coupons = Coupon.objects.filter(is_active=True, expired_at__lte=timezone.now())
    expired_coupons.update(is_active=False)


