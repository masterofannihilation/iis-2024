from django.http import HttpRequest
from .models import User


def logged_in_user(request: HttpRequest):
    context = {}
    context["logged_in_user"] = request.user
    if request.user.is_authenticated:
        user: User = request.user  # type: ignore
        context["logged_in_admin"] = user.role == User.Role.ADMINISTRATOR
        fullname = f"{user.first_name} {user.last_name}".strip()
        context["logged_in_user_fullname"] = f"({fullname})" if fullname != "" else ""

    return context
