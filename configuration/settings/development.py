import os
from .base import *
import cloudinary
import cloudinary_storage

DEBUG = False

ALLOWED_HOSTS = ['titaniumtraining.pythonanywhere.com',
                 '127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


CLOUDINARY_URL = 'cloudinary://387625877385614:zZrsexxvBVryHpiyJ6DG2tZrl5Y@dbrvleydy'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dbrvleydy',
    'API_KEY': '387625877385614',
    'API_SECRET': 'zZrsexxvBVryHpiyJ6DG2tZrl5Y',
}

# Media files
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
