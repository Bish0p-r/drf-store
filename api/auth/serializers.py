from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.user.models import User
from api.user.serializers import UserSerializer


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'bio', 'avatar', 'email', 'username', 'first_name', 'last_name', 'password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
