from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('Administrator', 'Administrator'),
        ('Caregiver', 'Caregiver'),
        ('Veterinarian', 'Veterinarian'),
        ('Volunteer', 'Volunteer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    contact_info = models.TextField(blank=True, null=True)

    # Add related_name to avoid conflicts with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='shelter_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='shelter_user_set',
        blank=True
    )

    def __str__(self):
        return self.username

class Animal(models.Model):
    ANIMAL_TYPES = (
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Rabbit', 'Rabbit'),
        ('Other', 'Other'),
    )
    
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=ANIMAL_TYPES)
    date_of_birth = models.DateField()
    description = models.TextField()
    intake_date = models.DateField()

    def __str__(self):
        return self.name

class Walk(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='walks')
    volunteer = models.ForeignKey(User, limit_choices_to={'role': 'Volunteer'}, on_delete=models.SET_NULL, null=True, blank=True, related_name='volunteer_walks')
    caregiver = models.ForeignKey(User, limit_choices_to={'role': 'Caregiver'}, on_delete=models.CASCADE, related_name='caregiver_walks')
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    STATUS_CHOICES = (
        ('Reserved', 'Reserved'),
        ('Approved', 'Approved'),
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Reserved')

    def __str__(self):
        return f"{self.animal.name} walk at {self.scheduled_time}"

class VeterinarianRequest(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='vet_requests')
    caregiver = models.ForeignKey(User, limit_choices_to={'role': 'Caregiver'}, on_delete=models.CASCADE, related_name='caregiver_requests')
    veterinarian = models.ForeignKey(User, limit_choices_to={'role': 'Veterinarian'}, on_delete=models.SET_NULL, null=True, blank=True, related_name='vet_requests')
    request_date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = (
        ('Requested', 'Requested'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Requested')
    examination_date = models.DateTimeField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Request for {self.animal.name} by {self.caregiver.username}"