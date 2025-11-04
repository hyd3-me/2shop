from django.test import TestCase
from shop.models import Role, BusinessElement, AccessRule
from shop.utils.access_rule_utils import create_access_rule


class AccessRuleUtilsTest(TestCase):
    def setUp(self):
        self.admin_role = Role.objects.create(name="admin")
        self.manager_role = Role.objects.create(name="manager")
        self.user_role = Role.objects.create(name="user")
        self.order_element = BusinessElement.objects.create(name="Order")

    def test_create_access_rule_admin(self):
        rule = create_access_rule(
            role=self.admin_role,
            business_element=self.order_element,
            create_permission=True,
            read_permission=True,
            update_permission=True,
            delete_permission=True,
            can_create_for_other_users=True,
        )
        self.assertTrue(rule.create_permission)
        self.assertTrue(rule.can_create_for_other_users)

    def test_create_access_rule_manager(self):
        rule = create_access_rule(
            role=self.manager_role,
            business_element=self.order_element,
            create_permission=True,
            read_permission=True,
            update_permission=True,
            delete_permission=False,
            can_create_for_other_users=True,
        )
        self.assertFalse(rule.delete_permission)
        self.assertTrue(rule.can_create_for_other_users)

    def test_create_access_rule_user(self):
        rule = create_access_rule(
            role=self.user_role,
            business_element=self.order_element,
            create_permission=True,
            read_permission=True,
            update_permission=False,
            delete_permission=False,
            can_create_for_other_users=False,
        )
        self.assertFalse(rule.can_create_for_other_users)
        self.assertEqual(rule.role.name, "user")

    def test_create_access_rule_duplicate_raises(self):
        create_access_rule(
            role=self.admin_role,
            business_element=self.order_element,
            create_permission=True,
        )
        with self.assertRaises(ValueError):
            create_access_rule(
                role=self.admin_role,
                business_element=self.order_element,
                create_permission=True,
            )
