from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from shelter.models import Animal, User
from shelter.seeds import animals


class AnimalTestBase(TestCase):
    def setUp(self):
        User = get_user_model()

        # Create users with different roles
        self.admin = User.objects.create_user(
            username="test_admin", password="password", role=User.Role.ADMINISTRATOR
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


class TestAnimalDetail(AnimalTestBase):
    def veriy_view(self):
        response = self.client.get(
            reverse("animal_detail", args=[animals.ANIMAL_SEEDS[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, animals.ANIMAL_SEEDS[0].name)

    def test_admin_can_view_animal_detail(self):
        self.login_as(self.admin)
        self.veriy_view()

    def test_caregiver_can_view_animal_detail(self):
        self.login_as(self.caregiver)
        self.veriy_view()

    def test_vet_can_view_animal_detail(self):
        self.login_as(self.veterinarian)
        self.veriy_view()

    def test_volunteer_can_view_animal_detail(self):
        self.login_as(self.volunteer)
        self.veriy_view()

    def test_guest_cant_view_animal_detail(self):
        self.client.logout()
        response = self.client.get(
            reverse("animal_detail", args=[animals.ANIMAL_SEEDS[0].id])
        )
        self.assertEqual(response.status_code, 200) 


class TestAnimalCreate(AnimalTestBase):
    def create_animal(self):
        data = {
            "name": "Bella",
            "species": "Cat",
            "date_of_birth": "2019-06-15",
            "description": "Calm and affectionate",
            "intake_date": "2023-11-10",
        }
        return self.client.post(reverse("animal_create"), data)

    def create_success(self):
        response = self.create_animal()
        self.assertEqual(response.status_code, 302)  # Successful redirect
        self.assertEqual(Animal.objects.count(), len(animals.ANIMAL_SEEDS) + 1)

    def create_unauth(self):
        response = self.create_animal()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Animal.objects.count(), len(animals.ANIMAL_SEEDS))

    def test_admin_can_create_animal(self):
        self.login_as(self.admin)
        self.create_success()

    def test_caregiver_can_create_animal(self):
        self.login_as(self.caregiver)
        self.create_success()

    def test_vet_cant_create_animal(self):
        self.login_as(self.veterinarian)
        self.create_unauth()

    def test_volunteer_cant_create_animal(self):
        self.login_as(self.volunteer)
        self.create_unauth()


class TestAnimalEdit(AnimalTestBase):
    def edit_animal(self):
        data = {
            "name": "Jambo",
            "species": "Cat",
            "date_of_birth": "2020-06-15",
            "description": "Updated description",
            "intake_date": "2023-10-20",
        }
        return self.client.post(
            reverse("animal_edit", args=[animals.ANIMAL_SEEDS[1].id]), data
        )

    def edit_success(self):
        response = self.edit_animal()
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse("animal_detail", args=[animals.ANIMAL_SEEDS[1].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Updated description")

    def edit_unauth(self):
        response = self.edit_animal()
        self.assertEqual(response.status_code, 403)

    def test_admin_can_edit_animal(self):
        self.login_as(self.admin)
        self.edit_success()

    def test_caregiver_can_edit_animal(self):
        self.login_as(self.caregiver)
        self.edit_success()

    def test_vet_cant_edit_animal(self):
        self.login_as(self.veterinarian)
        self.edit_unauth()

    def test_volunteer_cant_edit_animal(self):
        self.login_as(self.volunteer)
        self.edit_unauth()


class TestAnimalDelete(AnimalTestBase):
    def delete_success(self):
        response = self.client.post(
            reverse("animal_delete", args=[animals.ANIMAL_SEEDS[1].id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Animal.objects.count(), len(animals.ANIMAL_SEEDS) - 1)

    def delete_unauth(self):
        response = self.client.post(
            reverse("animal_delete", args=[animals.ANIMAL_SEEDS[1].id])
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Animal.objects.count(), len(animals.ANIMAL_SEEDS))

    def test_admin_can_delete_animal(self):
        self.login_as(self.admin)
        self.delete_success()

    def test_caregiver_can_delete_animal(self):
        self.login_as(self.caregiver)
        self.delete_success()

    def test_vet_cant_delete_animal(self):
        self.login_as(self.veterinarian)
        self.delete_unauth()

    def test_volunteer_cant_delete_animal(self):
        self.login_as(self.volunteer)
        self.delete_unauth()
