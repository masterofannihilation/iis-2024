from django import template
from ..models import User

register = template.Library()

@register.filter
def can_manage_animals(user):
    """Check if the user can manage animals."""
    return user.role in [User.Role.CAREGIVER, User.Role.ADMINISTRATOR]
