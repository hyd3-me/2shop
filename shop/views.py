from rest_framework import viewsets
from .models import Cart, Product, Category, Order
from rest_framework.permissions import AllowAny
from shop.permissions import AccessRulePermission, AccessRulePermissionProduct
from .serializers import (
    CartSerializer,
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AccessRulePermission]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AccessRulePermissionProduct]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
