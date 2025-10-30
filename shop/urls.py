from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, OrderViewSet

app_name = "shop"
router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
