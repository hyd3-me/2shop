from rest_framework.permissions import BasePermission, SAFE_METHODS
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

        return True
