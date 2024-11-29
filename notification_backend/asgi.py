import os

from django.core.asgi import get_asgi_application

from channels.security.websocket import AllowedHostsOriginValidator

from channels.routing import ProtocolTypeRouter, URLRouter

from middlewares.websocket_auth_middleware import WebsocketAuthMiddleware

from notification.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notification_backend.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            WebsocketAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
