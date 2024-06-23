import os
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

load_dotenv()
environment = os.environ.get('ENVIRONMENT')

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'configuration.settings'+environment)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
