from django import template
from ..models import User
from django.contrib.auth.models import AbstractUser

register = template.Library()


@register.filter
def can_manage_animals(user):
    """Check if the user can manage animals."""
    return user.role in [User.Role.CAREGIVER, User.Role.ADMINISTRATOR]


@register.filter
def can_manage_users(user: User | AbstractUser):
    """Check if the user can manage users."""
    if not user.is_authenticated:
        return False
    return user.role in [User.Role.CAREGIVER, User.Role.ADMINISTRATOR]  # type: ignore


@register.filter
def is_volunteer(user):
    """Check if the user is a volunteer."""
    return user.role == User.Role.VOLUNTEER


@register.filter
def is_vet(user):
    """Check if the user is a veterinarian."""
    return user.role == User.Role.VETERINARIAN
