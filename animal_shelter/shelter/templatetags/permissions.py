from django import template
from ..models import User

register = template.Library()


@register.filter
def can_manage_animals(user):
    """Check if the user can manage animals."""
    return user.role in [User.Role.CAREGIVER, User.Role.ADMINISTRATOR]


@register.filter
def is_volunteer(user):
    """Check if the user is a volunteer."""
    return user.role == User.Role.VOLUNTEER


@register.filter
def is_vet(user):
    """Check if the user is a veterinarian."""
    return user.role == User.Role.VETERINARIAN

@register.filter
def can_manage_walks(user):
    """Check if the user can manage walks."""
    return user.role in [User.Role.CAREGIVER, User.Role.ADMINISTRATOR]
