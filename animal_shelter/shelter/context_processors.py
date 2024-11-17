from django.http import HttpRequest
from .models import User


def logged_in_user(request: HttpRequest):
    context = {}
    context["logged_in_user"] = request.user
    if request.user.is_authenticated:
        context["logged_in_admin"] = request.user.role == User.Role.ADMINISTRATOR  # type: ignore

    return context
