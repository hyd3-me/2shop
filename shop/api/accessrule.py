from rest_framework import viewsets, permissions, serializers
from shop.models import AccessRule, Role, BusinessElement


class AccessRuleSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    business_element = serializers.PrimaryKeyRelatedField(
        queryset=BusinessElement.objects.all()
    )

    class Meta:
        model = AccessRule
        fields = [
            "id",
            "role",
            "business_element",
            "read_permission",
            "read_all_permission",
            "create_permission",
            "update_permission",
            "update_all_permission",
            "delete_permission",
            "delete_all_permission",
            "can_create_for_other_users",
        ]


class IsAdminRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.roles.filter(name="admin").exists()
        )


class AccessRuleViewSet(viewsets.ModelViewSet):
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    permission_classes = [IsAdminRolePermission]
