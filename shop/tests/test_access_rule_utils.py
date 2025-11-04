from django.test import TestCase
from shop.models import Role, BusinessElement, AccessRule
from shop.utils.access_rule_utils import create_access_rule, update_access_rule


class AccessRuleUtilsTest(TestCase):
    def setUp(self):
        self.admin_role = Role.objects.create(name="admin")
        self.manager_role = Role.objects.create(name="manager")
        self.user_role = Role.objects.create(name="user")
        self.order_element = BusinessElement.objects.create(name="Order")

    def _assert_rule_fields(self, rule, expected):
        self.assertEqual(rule.create_permission, expected["create_permission"])
        self.assertEqual(rule.read_permission, expected["read_permission"])
        self.assertEqual(rule.update_permission, expected["update_permission"])
        self.assertEqual(rule.delete_permission, expected["delete_permission"])
        self.assertEqual(
            rule.can_create_for_other_users, expected["can_create_for_other_users"]
        )
        self.assertEqual(
            rule.read_all_permission, expected.get("read_all_permission", False)
        )
        self.assertEqual(
            rule.update_all_permission, expected.get("update_all_permission", False)
        )
        self.assertEqual(
            rule.delete_all_permission, expected.get("delete_all_permission", False)
        )

    def test_create_access_rule_admin(self):
        expected = {
            "create_permission": True,
            "read_permission": True,
            "update_permission": True,
            "delete_permission": True,
            "can_create_for_other_users": True,
            "read_all_permission": False,
            "update_all_permission": False,
            "delete_all_permission": False,
        }
        rule = create_access_rule(
            role=self.admin_role, business_element=self.order_element, **expected
        )
        self._assert_rule_fields(rule, expected)

    def test_create_access_rule_manager(self):
        expected = {
            "create_permission": True,
            "read_permission": True,
            "update_permission": True,
            "delete_permission": False,
            "can_create_for_other_users": True,
            "read_all_permission": False,
            "update_all_permission": False,
            "delete_all_permission": False,
        }
        rule = create_access_rule(
            role=self.manager_role, business_element=self.order_element, **expected
        )
        self._assert_rule_fields(rule, expected)

    def test_create_access_rule_user(self):
        expected = {
            "create_permission": True,
            "read_permission": True,
            "update_permission": False,
            "delete_permission": False,
            "can_create_for_other_users": False,
            "read_all_permission": False,
            "update_all_permission": False,
            "delete_all_permission": False,
        }
        rule = create_access_rule(
            role=self.user_role, business_element=self.order_element, **expected
        )
        self._assert_rule_fields(rule, expected)

    def test_create_access_rule_duplicate_raises(self):
        create_access_rule(
            role=self.admin_role,
            business_element=self.order_element,
            create_permission=True,
            read_permission=True,
        )
        with self.assertRaises(ValueError):
            create_access_rule(
                role=self.admin_role,
                business_element=self.order_element,
                create_permission=True,
                read_permission=True,
            )

    def test_update_access_rule(self):
        rule = create_access_rule(
            role=self.admin_role,
            business_element=self.order_element,
            create_permission=True,
            read_permission=True,
            can_create_for_other_users=False,
        )
        updated_rule = update_access_rule(
            role=self.admin_role,
            business_element=self.order_element,
            can_create_for_other_users=True,
            create_permission=False,
        )
        self._assert_rule_fields(
            updated_rule,
            {
                "create_permission": False,
                "read_permission": True,
                "update_permission": False,
                "delete_permission": False,
                "can_create_for_other_users": True,
                "read_all_permission": False,
                "update_all_permission": False,
                "delete_all_permission": False,
            },
        )

    def test_update_access_rule_all_fields(self):
        rule = create_access_rule(
            role=self.admin_role,
            business_element=self.order_element,
            create_permission=True,
            read_permission=True,
            update_permission=False,
            delete_permission=False,
            can_create_for_other_users=False,
        )
        updated_rule = update_access_rule(
            role=self.admin_role,
            business_element=self.order_element,
            create_permission=False,
            read_permission=False,
            update_permission=True,
            delete_permission=True,
            can_create_for_other_users=True,
        )
        expected = {
            "create_permission": False,
            "read_permission": False,
            "update_permission": True,
            "delete_permission": True,
            "can_create_for_other_users": True,
            "read_all_permission": False,
            "update_all_permission": False,
            "delete_all_permission": False,
        }
        self._assert_rule_fields(updated_rule, expected)

    def test_update_access_rule_partial_fields(self):
        rule = create_access_rule(
            role=self.admin_role,
            business_element=self.order_element,
            create_permission=True,
            read_permission=True,
        )
        updated_rule = update_access_rule(
            role=self.admin_role,
            business_element=self.order_element,
            update_permission=True,
        )
        self.assertTrue(updated_rule.update_permission)
        self.assertTrue(updated_rule.create_permission)
        self.assertTrue(updated_rule.read_permission)

    def test_update_access_rule_nonexistent_raises(self):
        with self.assertRaises(ValueError):
            update_access_rule(
                role=self.manager_role,
                business_element=self.order_element,
                create_permission=True,
            )
