"""
WSGI config for findme_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findme_project.settings.production')

application = get_wsgi_application()
