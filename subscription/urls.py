from django.urls import path
from subscription.views import *

app_name = 'subscription'
urlpatterns = [
    path('initialize-transaction/', InitializeTransactionView.as_view(),
         name='initialize-transaction'),
    path('verify-transaction/<str:reference>/',
         VerifyTransactionView.as_view(), name='verify-transaction'),
    path('charge-authorization/', ChargeAuthorizationView.as_view(),
         name='charge-authorization'),
]
