from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

app_name = "shop"
router = DefaultRouter()
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
