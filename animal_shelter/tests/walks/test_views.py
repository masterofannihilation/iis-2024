from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from shelter.models import Walk
from shelter.seeds import animals, walks

class WalkTestBase(TestCase):
    def setUp(self):
        User = get_user_model()

        # Create users with different roles
        self.admin = User.objects.create_user(
            username="admin", password="password", role=User.Role.ADMINISTRATOR
        )
        self.caregiver = User.objects.create_user(
            username="caregiver", password="password", role=User.Role.CAREGIVER
        )
        self.veterinarian = User.objects.create_user(
            username="vet", password="password", role=User.Role.VETERINARIAN
        )
        self.volunteer = User.objects.create_user(
            username="volunteer", password="password", role=User.Role.VOLUNTEER
        )

        self.client = Client()

    def login_as(self, user):
        """Helper method to log in as a specific user."""
        self.client.logout()
        self.client.login(username=user.username, password="password")

class TestWalkCreate(WalkTestBase):
    def create_walk(self):
        data = {
            "animal": animals.ANIMAL_SEEDS[0].id,
            "volunteer": self.volunteer.id,
            "caregiver": self.caregiver.id,
            "begin_time": "2023-11-10T10:00",
            "end_time": "2023-11-10T12:00",
            "status": "Reserved",
        }
        return self.client.post(reverse("walk_create"), data)

    def create_success(self):
        response = self.create_walk()
        self.assertEqual(response.status_code, 302)  # Successful redirect
        self.assertEqual(Walk.objects.count(), len(walks.WALK_SEEDS) + 1)

    def create_unauth(self):
        response = self.create_walk()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Walk.objects.count(), len(walks.WALK_SEEDS))

    def test_admin_can_create_walk(self):
        self.login_as(self.admin)
        self.create_success()

    def test_caregiver_can_create_walk(self):
        self.login_as(self.caregiver)
        self.create_success()

    def test_vet_cant_create_walk(self):
        self.login_as(self.veterinarian)
        self.create_unauth()

    def test_volunteer_cant_create_walk(self):
        self.login_as(self.volunteer)
        self.create_unauth()

class TestWalkDetail(WalkTestBase):
    def test_walk_detail(self):
        self.login_as(self.admin)
        response = self.client.get(reverse("walk_detail", args=[walks.WALK_SEEDS[0].id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, walks.WALK_SEEDS[0].animal.name)

class TestWalkEdit(WalkTestBase):
    def edit_walk(self):
        data = {
            "animal": animals.ANIMAL_SEEDS[0].id,
            "volunteer": self.volunteer.id,
            "caregiver": self.caregiver.id,
            "begin_time": "2023-11-10T10:00",
            "end_time": "2023-11-10T12:00",
            "status": "Approved",
        }
        return self.client.post(reverse("walk_edit", args=[walks.WALK_SEEDS[0].id]), data)

    def edit_success(self):
        response = self.edit_walk()
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("walk_detail", args=[walks.WALK_SEEDS[0].id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved")

    def edit_unauth(self):
        response = self.edit_walk()
        self.assertEqual(response.status_code, 403)

    def test_admin_can_edit_walk(self):
        self.login_as(self.admin)
        self.edit_success()

    def test_caregiver_can_edit_walk(self):
        self.login_as(self.caregiver)
        self.edit_success()

    def test_vet_cant_edit_walk(self):
        self.login_as(self.veterinarian)
        self.edit_unauth()

    def test_volunteer_cant_edit_walk(self):
        self.login_as(self.volunteer)
        self.edit_unauth()

class TestWalkDelete(WalkTestBase):
    def delete_success(self):
        response = self.client.post(reverse("walk_delete", args=[walks.WALK_SEEDS[0].id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Walk.objects.count(), len(walks.WALK_SEEDS) - 1)

    def delete_unauth(self):
        response = self.client.post(reverse("walk_delete", args=[walks.WALK_SEEDS[0].id]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Walk.objects.count(), len(walks.WALK_SEEDS))

    def test_admin_can_delete_walk(self):
        self.login_as(self.admin)
        self.delete_success()

    def test_caregiver_can_delete_walk(self):
        self.login_as(self.caregiver)
        self.delete_success()

    def test_vet_cant_delete_walk(self):
        self.login_as(self.veterinarian)
        self.delete_unauth()

    def test_volunteer_cant_delete_walk(self):
        self.login_as(self.volunteer)
        self.delete_unauth()

class TestChooseWalk(WalkTestBase):  
    def choose_walk(self):
        return self.client.post(reverse("walks_list"), {'walk_id': walks.WALK_SEEDS[9].id, 'action': 'choose'})

    def choose_success(self):
        response = self.choose_walk()
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("walk_detail", args=[walks.WALK_SEEDS[9].id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reserved")

    def choose_unauth(self):
        response = self.choose_walk()
        self.assertEqual(response.status_code, 403)

    def test_volunteer_can_choose_walk(self):
        self.login_as(self.volunteer)
        self.choose_success()

    def test_admin_cant_choose_walk(self):
        self.login_as(self.admin)
        self.choose_unauth()

    def test_caregiver_cant_choose_walk(self):
        self.login_as(self.caregiver)
        self.choose_unauth()

    def test_vet_cant_choose_walk(self):
        self.login_as(self.veterinarian)
        self.choose_unauth()