from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from shelter.models import User


class CommonTestBase(TestCase):
    def setUp(self):
        # Create users with different roles
        self.admin = User.objects.create_user(
            username="test_admin", password="password", role=User.Role.ADMINISTRATOR
        )
        self.caregiver = User.objects.create_user(
            username="test_caregiver", password="password", role=User.Role.CAREGIVER
        )
        self.veterinarian = User.objects.create_user(
            username="test_vet", password="password", role=User.Role.VETERINARIAN
        )
        self.volunteer = User.objects.create_user(
            username="test_volunteer", password="password", role=User.Role.VOLUNTEER
        )
        self.unverified = User.objects.create_user(
            username="test_unverified", password="password", role=User.Role.UNVERIFIED
        )

        self.client = Client()

    def login_as(self, user):
        """Helper method to log in as a specific user."""
        self.client.logout()
        self.client.login(username=user.username, password="password")
