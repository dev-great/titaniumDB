import os
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application

load_dotenv()
environment = os.environ.get('ENVIRONMENT')

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'configuration.settings'+environment)

application = get_asgi_application()
