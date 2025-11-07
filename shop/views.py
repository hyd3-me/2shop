from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Cart, Product, Category, Order, AccessRule, User, Role
from shop.permissions import (
    AccessRulePermission,
    AccessRulePermissionProduct,
    AccessRulePermissionOrder,
    IsAdminRolePermission,
)
from .serializers import (
    CartSerializer,
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
    AccessRuleSerializer,
)
from users.serializers import UserWithRolesSerializer
from shop.utils.access_rule_utils import assign_role_to_user, remove_role_from_user


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
    permission_classes = [AccessRulePermissionOrder]

    def _hide_get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        if user.roles.filter(name__in=["admin", "manager"]).exists():
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class AccessRuleViewSet(viewsets.ModelViewSet):
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    permission_classes = [IsAdminRolePermission]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserWithRolesSerializer
    permission_classes = [IsAdminRolePermission]

    @action(detail=True, methods=["post"], url_path="remove-role")
    def remove_role(self, request, pk=None):
        role_id = request.data.get("role_id")
        if not role_id:
            return Response(
                {"detail": "role_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = self.get_object()
        role = get_object_or_404(Role, pk=role_id)

        if remove_role_from_user(user, role):
            return Response(
                {"detail": f"Role {role.name} removed from user."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": f"User does not have role {role.name}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"], url_path="assign-role")
    def assign_role(self, request, pk=None):
        role_id = request.data.get("role_id")
        if not role_id:
            return Response(
                {"detail": "role_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = self.get_object()
        role = get_object_or_404(Role, pk=role_id)
        if assign_role_to_user(user, role):
            return Response(
                {"detail": f"Role {role.name} assigned to user."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": f"User already has role {role.name}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
