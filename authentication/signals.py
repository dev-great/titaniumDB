from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


# PASSWORD RESET EMAIL
@ receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        inshopper_user = instance
        merge_data = {
            'titanium_training_user':  f"{reset_password_token.user.email}",
            'otp': f" {reset_password_token.key} "
        }
        html_body = render_to_string("otp_mail.html", merge_data)
        msg = EmailMultiAlternatives(subject="Titanium Training Password Reset", from_email=settings.EMAIL_HOST_USER, to=[
                                     reset_password_token.user.email], body=" ",)
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

    except Exception as e:
        logger.error(f"Error sending password reset email: {e}")
