from typing import Optional
from django.urls import reverse
from shelter.users.list import UserListModel
from shelter.models import User
from ..test_base import CommonTestBase


class UserTestBase(CommonTestBase):
    pass


class TestUserManagementAccess(UserTestBase):
    def setUp(self):
        super().setUp()
        self.management_pages: list[tuple[str, Optional[dict]]] = [
            ("users_list", None),
            ("user_detail", {"id": 1_001_004}),  # type: ignore
            ("user_edit", {"id": self.volunteer.id}),  # type: ignore
            ("user_create", None),
        ]

        self.profile_pages: list[tuple[str, Optional[dict]]] = [
            ("profile", None),
            ("profile_edit", None),
            ("change_password", None),
        ]

    def _assert_get_status_code(self, status_code: int, view_name: str, get_args):
        response = self.client.get(reverse(view_name, kwargs=get_args))
        self.assertEqual(
            response.status_code, status_code, f"URL: {view_name}, args={get_args}"
        )

    def _assert_user_access(
        self,
        user: Optional[User],
        status_code: int,
        pages: list[tuple[str, Optional[dict]]],
    ):
        self.client.logout()
        if user:
            self.login_as(user)

        for case in pages:
            self._assert_get_status_code(status_code, case[0], case[1])

    def test_access_to_user_management(self):
        self._assert_user_access(self.admin, 200, self.management_pages)
        self._assert_user_access(self.caregiver, 200, self.management_pages)
        self._assert_user_access(self.veterinarian, 403, self.management_pages)
        self._assert_user_access(self.volunteer, 403, self.management_pages)
        self._assert_user_access(self.unverified, 403, self.management_pages)
        self._assert_user_access(None, 302, self.management_pages)

    def test_access_to_profile(self):
        self._assert_user_access(self.admin, 200, self.profile_pages)
        self._assert_user_access(self.caregiver, 200, self.profile_pages)
        self._assert_user_access(self.veterinarian, 200, self.profile_pages)
        self._assert_user_access(self.volunteer, 200, self.profile_pages)
        self._assert_user_access(self.unverified, 200, self.profile_pages)
        self._assert_user_access(None, 302, self.profile_pages)


class TestUserListView(UserTestBase):
    def test_default(self):
        self.login_as(self.admin)
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text='<td><input type="checkbox"', count=10)

    def test_search(self):
        self.login_as(self.admin)
        searched = "m"
        response = self.client.get(reverse("users_list"), {"username": searched})
        self.assertEqual(response.status_code, 200)
        users: list[UserListModel] = response.context["users"]
        self.assertTrue(len(users) > 0)
        for u in users:
            self.assertTrue(u.username.startswith(searched))

    def test_change_role_as_admin(self):
        self.login_as(self.admin)
        user1 = User.objects.create_user(username="user1", password="password")
        user2 = User.objects.create_user(username="user2", password="password")
        user2.role = User.Role.CAREGIVER
        user2.save()

        new_role = User.Role.VETERINARIAN
        data = {
            "selected_users": [user1.id, user2.id],  # type: ignore
            "role": new_role.value,
            "change_role": "change_role",
        }

        response = self.client.post(reverse("users_list"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, text=f"Changed role of 2 users to {new_role.value}."
        )

        user1.refresh_from_db()
        user2.refresh_from_db()

        self.assertEqual(user1.role, new_role)
        self.assertEqual(user2.role, new_role)

    def test_change_role_as_caregiver(self):
        self.login_as(self.caregiver)
        user1 = User.objects.create_user(username="user1", password="password")
        user2 = User.objects.create_user(username="user2", password="password")
        self.assertEqual(user1.role, User.Role.UNVERIFIED)
        self.assertEqual(user2.role, User.Role.UNVERIFIED)

        new_role = User.Role.VOLUNTEER
        data = {
            "selected_users": [user1.id, user2.id],  # type: ignore
            "role": new_role.value,
            "change_role": "change_role",
        }

        response = self.client.post(reverse("users_list"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, text=f"Changed role of 2 users to {new_role.value}."
        )

        user1.refresh_from_db()
        user2.refresh_from_db()

        self.assertEqual(user1.role, new_role)
        self.assertEqual(user2.role, new_role)

    def test_change_role_as_caregiver_invalid(self):
        self.login_as(self.caregiver)
        user1 = User.objects.create_user(username="user1", password="password")
        user1.role = User.Role.VOLUNTEER
        user1.save()

        new_role = User.Role.VETERINARIAN
        data = {
            "selected_users": [user1.id],  # type: ignore
            "role": new_role.value,
            "change_role": "change_role",
        }

        response = self.client.post(reverse("users_list"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=f"Access Denied: Insufficient privileges.")

        user1.refresh_from_db()
        self.assertEqual(user1.role, User.Role.VOLUNTEER)

    def test_activate_as_admin(self):
        self.login_as(self.admin)
        user1 = User.objects.create_user(
            username="user1", password="password", is_active=True
        )
        user2 = User.objects.create_user(
            username="user2", password="password", is_active=False
        )
        user2.role = User.Role.CAREGIVER
        user2.save()

        data = {"selected_users": [user1.id, user2.id], "activate": "activate"}  # type: ignore

        response = self.client.post(reverse("users_list"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=f"Changed status of 2 users to active.")

        user1.refresh_from_db()
        user2.refresh_from_db()

        self.assertTrue(user1.is_active)
        self.assertTrue(user2.is_active)

    def test_activate_as_caregiver_invalid(self):
        self.login_as(self.caregiver)
        user1 = User.objects.create_user(
            username="user1", password="password", is_active=True
        )
        user2 = User.objects.create_user(
            username="user2", password="password", is_active=False
        )
        user2.role = User.Role.CAREGIVER
        user2.save()

        data = {"selected_users": [user1.id, user2.id], "activate": "activate"}  # type: ignore

        response = self.client.post(reverse("users_list"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=f"Access Denied: Insufficient privileges.")

        user1.refresh_from_db()
        user2.refresh_from_db()

        self.assertTrue(user1.is_active)
        self.assertFalse(user2.is_active)
