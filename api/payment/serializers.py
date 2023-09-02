from rest_framework import serializers


class CreatePaymentSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex')
    return_url = serializers.CharField(max_length=128)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)
    address = serializers.CharField(max_length=256)
