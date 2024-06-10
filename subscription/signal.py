import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from dotenv import load_dotenv
from rave_python import Rave

from subscription.models import Subscription

dotenv_path = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)
User = get_user_model()
rave = Rave(os.getenv("FLW_PUBLIC_KEY"), os.getenv("FLW_SECRET_KEY"))


@receiver(post_save, sender=Subscription)
def subscription_created(sender, instance, **kwargs):
    if instance.created:
        inshopper_user = Subscription.user
        merge_data = {
            'inshopper_user': f"{inshopper_user.email}",
            'msg': f" Hi {inshopper_user.email}, Welcome to Titanium Academy. We are glad to have you on board. "
        }
        html_body = render_to_string(
            "emails/sub_created.html", merge_data)
        msg = EmailMultiAlternatives(subject="Subscribed!", from_email=settings.EMAIL_HOST_USER, to=[
            instance.email], body=" ", )
        msg.attach_alternative(html_body, "text/html")
        return msg.send(fail_silently=False)


@receiver(post_save, sender=Subscription)
def send_subscription_expired(sender, instance, **kwargs):
    if instance.is_expired:
        inshopper_user = Subscription.user
        merge_data = {
            'inshopper_user': f"{inshopper_user.email}",
            'msg': f" Hi {inshopper_user.email}, Your subscription just expired. Please renew your subscription to "
            f"continue enjoying our services."
        }
        html_body = render_to_string(
            "emails/sub_expired.html", merge_data)
        msg = EmailMultiAlternatives(subject="Subscription Expired!", from_email=settings.EMAIL_HOST_USER, to=[
            instance.email], body=" ", )
        msg.attach_alternative(html_body, "text/html")
        return msg.send(fail_silently=False)
