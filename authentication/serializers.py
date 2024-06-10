from rest_framework import serializers, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password',
                  'first_name', 'last_name', 'phone_number', 'image', 'fcm_token', ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', "")
        password = data.get('password', "")
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise ValidationError(
                        "Your account has been suspended", code=404)
            else:
                raise ValidationError(
                    "Please check your credentials and try again!", code=401)
        else:
            raise ValidationError(
                "Please enter both username and password to login!", code=401)
        return data


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
