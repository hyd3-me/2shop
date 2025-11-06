from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import viewsets, permissions, serializers
from shop.models import AccessRule, BusinessElement


class AccessRulePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        element_name = "Category"
        try:
            element = BusinessElement.objects.get(name=element_name)
        except BusinessElement.DoesNotExist:
            return False

        user_roles = request.user.roles.all()

        if request.method in SAFE_METHODS:
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.read_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        if request.method == "POST":
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.create_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        if request.method in ["PUT", "PATCH"]:
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.update_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        elif request.method == "DELETE":
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.delete_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        return True


class AccessRulePermissionProduct(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        element_name = "Product"
        try:
            element = BusinessElement.objects.get(name=element_name)
        except BusinessElement.DoesNotExist:
            return False

        user_roles = request.user.roles.all()

        if request.method in SAFE_METHODS:
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.read_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        if request.method == "POST":
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.create_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        if request.method in ["PUT", "PATCH"]:
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.update_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        elif request.method == "DELETE":
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.delete_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        return True


class AccessRulePermissionOrder(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        element_name = "Order"
        try:
            element = BusinessElement.objects.get(name=element_name)
        except BusinessElement.DoesNotExist:
            return False

        user_roles = request.user.roles.all()

        if request.method in SAFE_METHODS:
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.read_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        if request.method == "POST":
            if request.method == "POST":
                user_id = request.data.get("user")

            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if (
                        str(request.user.id) != str(user_id)
                        and not rule.can_create_for_other_users
                    ):
                        return False
                    if rule.create_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        if request.method in ["PUT", "PATCH"]:
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.update_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        elif request.method == "DELETE":
            for role in user_roles:
                try:
                    rule = AccessRule.objects.get(role=role, business_element=element)
                    if rule.delete_permission:
                        return True
                except AccessRule.DoesNotExist:
                    continue
            return False

        return True

    def has_object_permission(self, request, view, obj):
        user_roles = request.user.roles.all()

        for role in user_roles:
            try:
                rule = AccessRule.objects.get(role=role, business_element__name="Order")
                if role.name in ["admin", "manager"]:
                    if request.method in SAFE_METHODS and rule.read_permission:
                        return True
                    if request.method in ["PUT", "PATCH"] and rule.update_permission:
                        return True
                    if request.method == "DELETE" and rule.delete_permission:
                        return True
                elif role.name == "user":
                    if obj.user == request.user:
                        if request.method in SAFE_METHODS and rule.read_permission:
                            return True
                        if (
                            request.method in ["PUT", "PATCH"]
                            and rule.update_permission
                        ):
                            return True
                        if request.method == "DELETE" and rule.delete_permission:
                            return True
            except AccessRule.DoesNotExist:
                continue
        return False


class IsAdminRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.roles.filter(name="admin").exists()
        )
