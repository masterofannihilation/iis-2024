from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Model
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRATOR = "Administrator", "Administrator"
        CAREGIVER = "Caregiver", "Caregiver"
        VETERINARIAN = "Veterinarian", "Veterinarian"
        VOLUNTEER = "Volunteer", "Volunteer"

        @staticmethod
        def from_string(s: str) -> "User.Role":
            for r in User.Role.choices:
                if r[1] == s:
                    return r[0]

            raise ValueError(f"{s} is not a valid role name")

        @staticmethod
        def from_string_safe(s: str) -> Optional["User.Role"]:
            for r in User.Role.choices:
                if r[1] == s:
                    return r[0]

            return None

    role = models.CharField(
        max_length=20,
        choices=Role.choices,  # Use the enumeration here
    )
    contact_info = models.TextField(blank=True, null=True)

    # Add related_name to avoid conflicts with auth.User
    groups = models.ManyToManyField(
        "auth.Group", related_name="shelter_user_set", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="shelter_user_set", blank=True
    )

    def is_authorized_enough(self, min_role: Role) -> bool:
        order = (
            User.Role.ADMINISTRATOR,
            User.Role.CAREGIVER,
            User.Role.VETERINARIAN,
            User.Role.VOLUNTEER,
        )
        # the lower the index the higher the privileges
        min_role_idx = order.index(min_role)
        self_role_idx = order.index(self.role)
        return self_role_idx <= min_role_idx

    def __str__(self):
        return self.username


class Animal(models.Model):
    class AnimalType(models.TextChoices):
        DOG = "Dog", "Dog"
        CAT = "Cat", "Cat"
        RABBIT = "Rabbit", "Rabbit"
        OTHER = "Other", "Other"

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=AnimalType.choices)
    date_of_birth = models.DateField()
    description = models.TextField()
    intake_date = models.DateField()
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Walk(models.Model):
    class Status(models.TextChoices):
        RESERVED = "Reserved", "Reserved"
        APPROVED = "Approved", "Approved"
        BORROWED = "Borrowed", "Borrowed"
        RETURNED = "Returned", "Returned"
        AVAILABLE = "Available", "Available"

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="walks")
    volunteer = models.ForeignKey(
        User,
        limit_choices_to={"role": "Volunteer"},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="volunteer_walks",
    )
    caregiver = models.ForeignKey(
        User,
        limit_choices_to={"role": "Caregiver"},
        on_delete=models.CASCADE,
        related_name="caregiver_walks",
    )
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.RESERVED
    )

    def __str__(self):
        return f"{self.animal.name} walk at {self.begin_time}"
    
    def can_be_chosen_by_volunteer(self):
        return self.status == self.Status.AVAILABLE

    def can_be_approved_by_caregiver(self):
        return self.status == self.Status.RESERVED


class VeterinarianRequest(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "Requested", "Requested"
        SCHEDULED = "Scheduled", "Scheduled"
        COMPLETED = "Completed", "Completed"

    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="vet_requests"
    )
    caregiver = models.ForeignKey(
        User,
        limit_choices_to={"role": "Caregiver"},
        on_delete=models.CASCADE,
        related_name="caregiver_requests",
    )
    veterinarian = models.ForeignKey(
        User,
        limit_choices_to={"role": "Veterinarian"},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vet_requests",
    )
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.REQUESTED
    )
    examination_date = models.DateTimeField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Request for {self.animal.name} by {self.caregiver.username}"
