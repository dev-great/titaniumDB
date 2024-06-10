from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
import datetime
from datetime import timedelta
from datetime import datetime as dt

from authentication.models import CustomUser

today = datetime.date.today()


# User Payment History
class PayHistory(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, default=None)
    paystack_charge_id = models.CharField(
        max_length=100, default='', blank=True)
    paystack_access_code = models.CharField(
        max_length=100, default='', blank=True)
    payment_for = models.ForeignKey(
        'Membership', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# Membership


class Membership(models.Model):
    # Note that they are all capitalize//
    MEMBERSHIP_CHOICES = (
        ('Premium', 'Premium'),
        ('Standard', 'Standard'),
        ('Basic', 'Basic'),
    )
    PERIOD_DURATION = (
        ('Months', 'Months'),
        ('Years', 'Years'),
    )
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
    duration = models.PositiveIntegerField(default=30)
    duration_period = models.CharField(
        max_length=100, default='Months', choices=PERIOD_DURATION)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.membership_type

# User Membership


class UserMembership(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(
        Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
    reference_code = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=UserMembership)
def create_subscription(sender, instance, *args, **kwargs):
    if instance:
        Subscription.objects.create(user_membership=instance, expires_in=dt.now(
        ).date() + timedelta(days=instance.membership.duration))


# User Subscription
class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, related_name='subscription', on_delete=models.CASCADE, default=None)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username


@receiver(post_save, sender=Subscription)
def update_active(sender, instance, *args, **kwargs):
    if instance.expires_in < today:
        subscription = Subscription.objects.get(id=instance.id)
        subscription.delete()


class Card(models.Model):
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, default=None)
    authorization_code = models.CharField(max_length=255)
    card_type = models.CharField(max_length=50)
    last4 = models.CharField(max_length=4)
    exp_month = models.CharField(max_length=2)
    exp_year = models.CharField(max_length=4)
    bin = models.CharField(max_length=6)
    bank = models.CharField(max_length=100)
    channel = models.CharField(max_length=50)
    signature = models.CharField(max_length=255)
    reusable = models.BooleanField(default=False)
    country_code = models.CharField(max_length=2)
    account_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.account_name} - {self.card_type} {self.last4}"
