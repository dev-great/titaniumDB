# views.py
import os
import logging
import random
from rest_framework.generics import DestroyAPIView
from django.shortcuts import get_object_or_404
from authentication.models import CustomUser
from exceptions.custom_apiexception_class import *
from utils.custom_response import custom_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from dotenv import load_dotenv
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from .serializers import ChangePasswordSerializer, UserSerializer, TokenObtainPairResponseSerializer, TokenRefreshResponseSerializer, TokenVerifyResponseSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
logger = logging.getLogger(__name__)

load_dotenv()
User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={status.HTTP_201_CREATED: UserSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            logger.info(f"User registered: {serializer.data['email']}")
            return custom_response(status_code=status.HTTP_201_CREATED, message="Success", data=response_data)
        else:
            error_msg = str(serializer.errors)
            logger.error(f"Registration error: {error_msg}")
            return CustomAPIException(detail=str(serializer.errors), status_code=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid credentials.",
        }
    )
    def post(self, request, *args, **kwargs):
        logger.info("Login request received.")
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            logger.info("Request data is valid.")
        except TokenError as e:
            logger.error(f"TokenError encountered: {e}")
            raise CustomAPIException(
                detail="Invalid token.", status_code=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f"Exception encountered: {e}")
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST)

        logger.info("Login successful.")
        return custom_response(status_code=status.HTTP_200_OK, message="Success", data=serializer.validated_data)


class TokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid token.",
        }
    )
    def post(self, request, *args, **kwargs):
        logger.info("Token refresh request received.")
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            logger.info("Token refresh successful.")
            return custom_response(status_code=status.HTTP_200_OK, message="Token is refresh.", data=response.data)
        else:
            logger.error(
                f"Token refresh failed with status code {response.status_code}.")
            return CustomAPIException(detail="Token is invalid.", status_code=response.status_code, data=response.data)


class TokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid token.",
        }
    )
    def post(self, request, *args, **kwargs):
        logger.info("Token verification request received.")
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            logger.info("Token verification successful.")
            return custom_response(status_code=status.HTTP_200_OK, message="Token is valid.", data=response.data)
        else:
            logger.error(
                f"Token verification failed with status code {response.status_code}.")
            return CustomAPIException(detail="Token is invalid or expired.", status_code=response.status_code, data=response.data)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    csrf_protect_method = method_decorator(csrf_protect)

    @swagger_auto_schema(request_body=UserSerializer)
    def patch(self, request):
        logger.info(
            f"UserProfile PATCH request received for user: {request.user.email}")
        user_email = request.user.email

        try:
            profile = CustomUser.objects.get(email__exact=user_email)
            logger.debug(f"User profile found for email: {user_email}")
        except CustomUser.DoesNotExist:
            logger.error(f"User profile not found for email: {user_email}")
            raise CustomAPIException(
                detail="User profile not found.", status_code=status.HTTP_404_NOT_FOUND)

        serializers = UserSerializer(profile, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            logger.info(
                f"User profile updated successfully for email: {user_email}")
            return custom_response(status_code=status.HTTP_200_OK, message="User updated successfully", data=serializers.data)

        logger.error(
            f"User profile update failed for email: {user_email}, errors: {serializers.errors}")
        raise CustomAPIException(
            detail=serializers.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        logger.info(
            f"UserProfile GET request received for user: {request.user.email}")
        email = request.user.email

        try:
            profile = CustomUser.objects.get(email__exact=email)
            logger.debug(f"User profile found for email: {email}")
        except CustomUser.DoesNotExist:
            logger.error(f"User profile not found for email: {email}")
            raise CustomAPIException(
                detail="User profile not found.", status_code=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(profile)
        logger.info(f"User profile retrieved successfully for email: {email}")
        return custom_response(status_code=status.HTTP_200_OK, message="Success.", data=serializer.data)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'refresh', openapi.IN_QUERY, description="Refresh token", type=openapi.TYPE_STRING, required=True
            )
        ],
        responses={
            status.HTTP_205_RESET_CONTENT: "Logout successful.",
            status.HTTP_400_BAD_REQUEST: "Bad request, typically because of a malformed request body.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized, typically because of invalid credentials.",
        }
    )
    def post(self, request):
        logger.info(
            f"Logout POST request received for user: {request.user.email}")

        try:
            refresh_token = request.data['refresh']
            logger.debug(f"Refresh token received: {refresh_token}")

            token = RefreshToken(refresh_token)
            token.blacklist()

            logger.info(
                f"Token blacklisted successfully for user: {request.user.email}")
            return custom_response(status_code=status.HTTP_205_RESET_CONTENT, message="Logout successful.", data=None)

        except Exception as e:
            logger.error(
                f"Logout failed for user: {request.user.email}, error: {str(e)}")
            raise CustomAPIException(detail=str(
                e), status_code=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        logger.info(
            f"ChangePassword update request received for user: {request.user.email}")

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                logger.warning(
                    f"Invalid old password provided by user: {request.user.email}")
                return CustomAPIException(
                    detail="Invalid Credential",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    data={"old_password": ["Wrong password."]}
                )

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            logger.info(
                f"Password updated successfully for user: {request.user.email}")

            return custom_response(status_code=status.HTTP_200_OK, message='Password updated successfully', data=None)

        logger.error(
            f"Password update failed for user: {request.user.email}, errors: {serializer.errors}")
        return CustomAPIException(detail=str(serializer.errors), status_code=status.HTTP_400_BAD_REQUEST)


class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        user_email = self.request.user.email
        logger.info(f"Fetching user object for email: {user_email}")
        return get_object_or_404(CustomUser, email=user_email)

    def delete(self, request, *args, **kwargs):
        try:
            user_email = request.user.email
            logger.info(f"Delete request received for user: {user_email}")

            paysita_user = self.get_object()
            self.perform_destroy(paysita_user)
            logger.info(f"User deleted successfully: {user_email}")

            return custom_response(status_code=status.HTTP_200_OK, message="User deleted", data=None)
        except CustomUser.DoesNotExist:
            logger.warning(f"User not found for email: {user_email}")
            return CustomAPIException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting user {user_email}: {str(e)}")
            return CustomAPIException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_destroy(self, instance):
        instance.delete()
        logger.info(f"User instance deleted: {instance.email}")


otp_storage = {}


class EmailOTPAuthentication(APIView):
    def post(self, request):
        email = request.data.get('email')

        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

        # Store the OTP with the email as the key
        otp_storage[email] = otp

        merge_data = {
            'inshopper_user': request.user.email,
            'otp': otp,
        }
        html_body = render_to_string(
            "emails/otp_mail.html", merge_data)
        msg = EmailMultiAlternatives(
            subject="Email Verification OTP.",
            from_email=os.getenv('EMAIL_USER'),
            to=[request.user.email],
            body=" ",
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

        return custom_response(status_code=status.HTTP_200_OK, message="OTP sent to your email.", data=None)

    def put(self, request):
        email = request.data.get('email')
        otp_entered = request.data.get('otp')

        if email not in otp_storage:
            return CustomAPIException(detail="OTP not sent for this email.", status_code=status.HTTP_400_BAD_REQUEST)

        if otp_entered == otp_storage[email]:
            del otp_storage[email]
            return custom_response(status_code=status.HTTP_200_OK, message="Email verification successful.", data=None)
        else:
            return CustomAPIException(detail="Incorrect OTP.", status_code=status.HTTP_400_BAD_REQUEST)
