import os
import django
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trosgate.settings")
django.setup()

import notification.routing

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
      URLRouter(notification.routing.websocket_urlpatterns)
    ),
})


# application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
#   "websocket": AllowedHostsOriginValidator(
#     AuthMiddlewareStack(URLRouter(notification.routing.websocket_urlpatterns)
#     ),
#   ),
# })




