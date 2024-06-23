import os
from datetime import timedelta
from uuid import uuid4
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
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
        token = os.environ.get('PAYSTACK_SECRET_KEY')
        headers = {
            'Authorization': f'Bearer {token}',
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
        token = os.environ.get('PAYSTACK_SECRET_KEY')
        headers = {
            'Authorization': f'Bearer {token}',
        }

        try:
            response = requests.get(url, headers=headers)
            response_data = response.json()
            if response.status_code == 200 and response_data['status']:
                authorization_data = response_data['data']['authorization']

                # Assuming you have the user's ID in the request or elsewhere
                user_id = request.user.id
                user = get_object_or_404(CustomUser, id=user_id)

                card = Card.objects.create(
                    user_id=user,
                    authorization_code=authorization_data['authorization_code'],
                    card_type=authorization_data['card_type'],
                    last4=authorization_data['last4'],
                    exp_month=authorization_data['exp_month'],
                    exp_year=authorization_data['exp_year'],
                    bin=authorization_data['bin'],
                    bank=authorization_data['bank'],
                    channel=authorization_data['channel'],
                    signature=authorization_data['signature'],
                    reusable=authorization_data['reusable'],
                    country_code=authorization_data['country_code'],
                    account_name=authorization_data['account_name'] or ''
                )

                card.save()
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"message": "An error occurred while connecting to Paystack.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChargeAuthorizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        card = get_object_or_404(Card, user_id=request.user)
        url = 'https://api.paystack.co/transaction/charge_authorization'
        token = os.environ.get('PAYSTACK_SECRET_KEY')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "email": request.data.get("email"),
            "amount": request.data.get("amount"),
            "authorization_code": card.authorization_code
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
