from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CartViewSet,
    CategoryViewSet,
    ProductViewSet,
    OrderViewSet,
    AccessRuleViewSet,
)

app_name = "shop"
router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"cart", CartViewSet)
router.register(r"accessrules", AccessRuleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
