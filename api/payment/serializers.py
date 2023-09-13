from rest_framework import serializers

from api.payment.models import Coupon


class CreatePaymentSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex', required=True)
    return_url = serializers.CharField(max_length=128, required=True)
    first_name = serializers.CharField(max_length=64, required=True)
    last_name = serializers.CharField(max_length=64, required=True)
    address = serializers.CharField(max_length=256, required=True)
    coupon = serializers.CharField(max_length=128, required=False)

    def validate_coupon(self, value):
        if not Coupon.objects.filter(code=value, is_active=True).exists():
            raise serializers.ValidationError("The coupon is invalid.")
        return value
