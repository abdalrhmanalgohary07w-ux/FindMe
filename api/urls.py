from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MissingPersonViewSet

router = DefaultRouter()
router.register(r'missing-persons', MissingPersonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
