"""
ASGI config for findme_project project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findme_project.settings.production')

application = get_asgi_application()
