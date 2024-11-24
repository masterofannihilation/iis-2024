from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from shelter.models import VeterinarianRequest, Animal, User
from shelter.seeds import health_records
from ..test_base import CommonTestBase

class HealthRecordTestBase(CommonTestBase):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def login_as(self, user):
        """Helper method to log in as a specific user."""
        self.client.logout()
        self.client.login(username=user.username, password="password")


class TestHealthRecordDetail(HealthRecordTestBase):
    def verify_view(self):
        response = self.client.get(
            reverse("health_records_detail", args=[health_records.HEALTH_RECORD_SEEDS[0].animal_id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, health_records.HEALTH_RECORD_SEEDS[0].result)

    def test_admin_can_view_health_record_detail(self):
        self.login_as(self.admin)
        self.verify_view()

    def test_caregiver_can_view_health_record_detail(self):
        self.login_as(self.caregiver)
        self.verify_view()

    def test_vet_can_view_health_record_detail(self):
        self.login_as(self.veterinarian)
        self.verify_view()

    def test_volunteer_can_view_health_record_detail(self):
        self.login_as(self.volunteer)
        self.verify_view()

    def test_guest_cant_view_health_record_detail(self):
        self.client.logout()
        response = self.client.get(
            reverse("health_records_detail", args=[health_records.HEALTH_RECORD_SEEDS[0].animal_id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login


class TestHealthRecordCreate(HealthRecordTestBase):
    def create_health_record(self):
        data = {
            "animal": health_records.HEALTH_RECORD_SEEDS[0].animal_id,
            "veterinarian": self.veterinarian.id,
            "status": VeterinarianRequest.Status.REQUESTED,
        }
        return self.client.post(reverse("health_records_create"), data)

    def create_success(self):
        response = self.create_health_record()
        self.assertEqual(response.status_code, 302)  # Successful redirect
        self.assertEqual(VeterinarianRequest.objects.count(), len(health_records.HEALTH_RECORD_SEEDS) + 1)

    def create_unauth(self):
        response = self.create_health_record()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(VeterinarianRequest.objects.count(), len(health_records.HEALTH_RECORD_SEEDS))

    def test_admin_cant_create_health_record(self):
        self.login_as(self.admin)
        self.create_unauth()

    def test_caregiver_can_create_health_record(self):
        self.login_as(self.caregiver)
        self.create_success()

    def test_vet_cant_create_health_record(self):
        self.login_as(self.veterinarian)
        self.create_unauth()

    def test_volunteer_cant_create_health_record(self):
        self.login_as(self.volunteer)
        self.create_unauth()


class TestHealthRecordEdit(HealthRecordTestBase):
    def edit_health_record_as_vet(self):
        data = {
            "status": VeterinarianRequest.Status.COMPLETED,
            "examination_date": "2025-11-15T10:00",
            "result": "Updated result",
        }
        return self.client.post(
            reverse("health_records_vet_edit", args=[health_records.HEALTH_RECORD_SEEDS[1].id]), data
        )

    def edit_health_record_as_caregiver(self):
        data = {
            "animal": health_records.HEALTH_RECORD_SEEDS[1].animal_id,
            "veterinarian": self.veterinarian.id,
            "status": VeterinarianRequest.Status.SCHEDULED,
        }
        return self.client.post(
            reverse("health_records_caregiver_edit", args=[health_records.HEALTH_RECORD_SEEDS[1].id]), data
        )

    def edit_success_as_vet(self):
        response = self.edit_health_record_as_vet()
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse("health_records_detail", args=[health_records.HEALTH_RECORD_SEEDS[1].animal_id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Updated result")

    def edit_success_as_caregiver(self):
        response = self.edit_health_record_as_caregiver()
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse("health_records_detail", args=[health_records.HEALTH_RECORD_SEEDS[1].animal_id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, VeterinarianRequest.Status.SCHEDULED)

    def edit_unauth(self):
        response = self.edit_health_record_as_vet()
        self.assertEqual(response.status_code, 403)

    def test_admin_cant_edit_health_record(self):
        self.login_as(self.admin)
        self.edit_unauth()

    def test_caregiver_can_edit_health_record(self):
        self.login_as(self.caregiver)
        self.edit_success_as_caregiver()

    def test_vet_can_edit_health_record(self):
        self.login_as(self.veterinarian)
        self.edit_success_as_vet()

    def test_volunteer_cant_edit_health_record(self):
        self.login_as(self.volunteer)
        self.edit_unauth()


class TestHealthRecordDelete(HealthRecordTestBase):
    def delete_success(self):
        response = self.client.post(
            reverse("health_records_delete", args=[health_records.HEALTH_RECORD_SEEDS[1].id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(VeterinarianRequest.objects.count(), len(health_records.HEALTH_RECORD_SEEDS) - 1)

    def delete_unauth(self):
        response = self.client.post(
            reverse("health_records_delete", args=[health_records.HEALTH_RECORD_SEEDS[1].id])
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(VeterinarianRequest.objects.count(), len(health_records.HEALTH_RECORD_SEEDS))

    def test_admin_cant_delete_health_record(self):
        self.login_as(self.admin)
        self.delete_unauth()

    def test_caregiver_can_delete_health_record(self):
        self.login_as(self.caregiver)
        self.delete_success()

    def test_vet_can_delete_health_record(self):
        self.login_as(self.veterinarian)
        self.delete_success()

    def test_volunteer_cant_delete_health_record(self):
        self.login_as(self.volunteer)
        self.delete_unauth()
