"""
ASGI config for quiz project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django import setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
setup()

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
import quiz.routing



#application = get_asgi_application()
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter( {
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack( URLRouter( quiz.routing.websocket_urlpatterns ) ),
} )
