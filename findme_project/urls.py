"""
URL configuration for findme_project project.
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import JsonResponse

urlpatterns = [
    path('', lambda r: JsonResponse({'message': 'Welcome to FindMe API', 'status': 'Running'})),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
