# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.homepage.urls import websocket_url
# from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        websocket_url
    )
})
