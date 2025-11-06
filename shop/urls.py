from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CartViewSet,
    CategoryViewSet,
    ProductViewSet,
    OrderViewSet,
    AccessRuleViewSet,
    UserViewSet,
)

app_name = "shop"
router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"cart", CartViewSet)
router.register(r"accessrules", AccessRuleViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
