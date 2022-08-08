"""
ASGI config for cmdb_hls project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb_hls.settings')
from django.core.asgi import get_asgi_application
# from job_manager.views.action import hls_log_action

django_application = get_asgi_application()

#
# async def application(scope, receive, send):
#     if scope['type'] == 'http':
#         await django_application(scope, receive, send)
#     elif scope['type'] == 'websocket':
#         # await hls_log_action(scope, receive, send)
#         pass
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")
