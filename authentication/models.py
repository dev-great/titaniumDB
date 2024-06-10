import uuid
import secrets
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


def get_image_upload_path(instance, filename):
    folder_path = f"titanium_training/user/{timezone.now().strftime('%Y/%m/%d')}/"
    return folder_path + filename


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(
        max_length=50, null=True, blank=True)
    last_name = models.CharField(
        max_length=50, null=True, blank=True)
    image = models.ImageField(
        upload_to=get_image_upload_path, null=True, blank=True)
    phone_number = models.CharField(
        max_length=15, null=True, blank=True)
    fcm_token = models.CharField(
        max_length=50, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    PASSWORD_FIELD = 'password'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'phone_number', 'image', 'fcm_token']

    def __str__(self):
        return str(self.email)
