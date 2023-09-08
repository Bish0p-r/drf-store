import json

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.cart.models import Cart

from api.payment.serializers import CreatePaymentSerializer
from api.payment.services import yookassa_create_order, payment_acceptance


class CreatePaymentView(CreateAPIView):
    serializer_class = CreatePaymentSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(summary='Создать платеж через Yookassa.', methods=["POST"])
    def post(self, request, *args, **kwargs):
        """
        Создание заказа и ссылки для оплаты.
        - POST /api/payment_create/
        """
        cart = Cart.objects.filter(user__public_id=request.POST['id'])

        if not cart.exists():
            return Response({"rejection": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreatePaymentSerializer(data=request.POST)

        if serializer.is_valid():
            serializer_data = serializer.validated_data
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        confirmation_url = yookassa_create_order(serializer_data)

        return Response(data={"confirmation_url": confirmation_url}, status=status.HTTP_200_OK)


class CreatePaymentAcceptanceView(CreateAPIView):
    @extend_schema(summary='Получение уведомлений от Yookassa.', methods=["POST"])
    def post(self, request, *args, **kwargs):
        """
        Получение уведомлений от Yookassa и изменение статус заказа.
        - POST /api/payment_acceptance/
        """
        response = json.loads(request.body)

        if payment_acceptance(response):
            return Response(200)
        return Response(404)
