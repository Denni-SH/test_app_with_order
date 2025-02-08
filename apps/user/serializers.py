from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'public_id', 'username', 'email', 'address', 'phone_number', 'date_of_birth', 'full_name',
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username, password = attrs.get('username'), attrs.get('password')
        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if user is None:
            raise AuthenticationFailed("Incorrect authentication credentials.")
        if not user.is_active:
            raise AuthenticationFailed("Please confirm your email address")

        refresh = self.get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        update_last_login(None, user)

        return data
