"""
ASGI config for bookstore-api-API project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this static1, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore-api.settings')

application = get_asgi_application()
