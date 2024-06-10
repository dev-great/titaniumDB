import os
from datetime import timedelta
from uuid import uuid4
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
from drf_yasg.utils import swagger_auto_schema
from rave_python import Rave, RaveExceptions
import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

User = get_user_model()
load_dotenv()


def reference_code_generator():
    uuid_4 = str(uuid4())
    current_date = str(datetime.now().strftime("%Y%m%d"))
    return "inshopper_" + uuid_4.replace("-", "")[:10] + current_date


class InitializeTransactionView(APIView):
    def post(self, request):
        email = request.data.get('email')
        amount = request.data.get('amount')

        if not email or not amount:
            return Response({"message": "Email and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            "email": email,
            "amount": amount
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            if response.status_code == 200:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"message": "An error occurred while connecting to Paystack.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyTransactionView(APIView):
    def get(self, request, reference):
        url = f'https://api.paystack.co/transaction/verify/{reference}'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        }

        try:
            response = requests.get(url, headers=headers)
            response_data = response.json()
            if response.status_code == 200:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"message": "An error occurred while connecting to Paystack.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChargeAuthorizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        url = 'https://api.paystack.co/transaction/charge_authorization'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            "email": request.data.get("email"),
            "amount": request.data.get("amount"),
            "authorization_code": request.data.get("authorization_code")
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            if response.status_code == 200:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"message": "An error occurred while connecting to Paystack.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
