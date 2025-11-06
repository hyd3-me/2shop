from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from shop.models import User, Role, BusinessElement, AccessRule


class AdminAccessRuleAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_role = Role.objects.create(name="admin")
        self.user_role = Role.objects.create(name="user")
        self.manager_role = Role.objects.create(name="manager")

        self.business_element = BusinessElement.objects.create(name="Order")

        self.admin_user = User.objects.create_user(
            email="admin@example.com", password="adminpass"
        )
        self.admin_user.roles.add(self.admin_role)

        self.normal_user = User.objects.create_user(
            email="user@example.com", password="userpass"
        )
        self.normal_user.roles.add(self.user_role)

        self.access_rule = AccessRule.objects.create(
            role=self.user_role,
            business_element=self.business_element,
            create_permission=True,
            read_permission=True,
        )

        self.client.force_authenticate(user=self.admin_user)

    def test_admin_can_get_user_access_rules(self):
        url = reverse("shop:accessrule-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        roles_in_response = [r["role"] for r in response.json()]
        self.assertIn(self.user_role.id, roles_in_response)

    def test_admin_can_update_access_rule(self):
        url = reverse("shop:accessrule-detail", kwargs={"pk": self.access_rule.pk})
        data = {
            "create_permission": False,
            "read_permission": False,
            "update_permission": True,
            "delete_permission": False,
            "read_all_permission": False,
            "update_all_permission": False,
            "delete_all_permission": False,
            "can_create_for_other_users": False,
            "role": self.user_role.id,
            "business_element": self.business_element.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["update_permission"], True)

    def test_admin_can_remove_specific_role_from_user(self):
        url = reverse("shop:user-remove-role", kwargs={"pk": self.normal_user.id})
        data = {"role_id": self.user_role.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.normal_user.refresh_from_db()
        self.assertNotIn(self.user_role, self.normal_user.roles.all())

    def test_admin_can_assign_specific_role_to_user(self):
        url = reverse("shop:user-assign-role", kwargs={"pk": self.normal_user.id})
        data = {"role_id": self.manager_role.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.normal_user.refresh_from_db()
        self.assertIn(self.user_role, self.normal_user.roles.all())
