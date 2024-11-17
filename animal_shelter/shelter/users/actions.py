import random
from typing import Optional

from django.http import HttpResponseForbidden
from ..models import User
import string


def generate_password() -> str:
    pwd = ""
    chars = string.ascii_letters + string.digits
    for i in range(12):
        pwd += random.choice(chars)
    return pwd


class ActionOverUsers:
    def __init__(self, requested_by: User) -> None:
        self.requested_by = requested_by
        self.result = None
        self.msg: str = "No action has been made."

    def _can_modify(self, modified_user: User) -> bool:
        if self.requested_by == modified_user:
            return False
        if self.requested_by.role == User.Role.ADMINISTRATOR:
            return True
        elif (
            self.requested_by.role == User.Role.CAREGIVER
            and modified_user.role == User.Role.VOLUNTEER
        ):
            return True
        else:
            return False

    def _retrieve_users(self, ids: list[int]) -> list[User]:
        return User.objects.filter(id__in=ids)  # type: ignore

    def _retrieve_and_authorize(
        self, ids: list[int]
    ) -> list[User] | HttpResponseForbidden:
        users = self._retrieve_users(ids)
        for u in users:
            if not self._can_modify(u):
                self.result = HttpResponseForbidden(
                    "Access Denied: Insufficient privileges."
                )
                self.msg = "Access Denied: Insufficient privileges."
                return self.result
        return users

    def set_active_state(
        self, set_active: bool, ids: list[int]
    ) -> Optional[HttpResponseForbidden]:
        users = self._retrieve_and_authorize(ids)
        if isinstance(users, HttpResponseForbidden):
            return users

        for u in users:
            u.is_active = set_active
            u.save()

        self.result = True
        state_str = "active" if set_active else "deactivated"
        self.msg = f"Changed status of {len(users)} users to {state_str}."

    def delete(self, ids: list[int]) -> Optional[HttpResponseForbidden]:
        users = self._retrieve_and_authorize(ids)
        if isinstance(users, HttpResponseForbidden):
            return users

        for u in users:
            u.delete()

        self.result = True
        self.msg = f"Deleted {len(users)} users."

    def change_role(
        self, role: User.Role, ids: list[int]
    ) -> Optional[HttpResponseForbidden]:
        users = self._retrieve_and_authorize(ids)
        if isinstance(users, HttpResponseForbidden):
            self.result = users
            return self.result

        if self.requested_by.role != User.Role.ADMINISTRATOR:
            return HttpResponseForbidden("Access Denied: Insufficient privileges.")

        for u in users:
            u.role = role
            u.save()

        self.result = True
        self.msg = f"Changed role of {len(users)} users to {role}."

    def reset_password(
        self, ids: list[int]
    ) -> list[tuple[User, str]] | HttpResponseForbidden:
        users = self._retrieve_and_authorize(ids)
        if isinstance(users, HttpResponseForbidden):
            return users

        result: list[tuple[User, str]] = []
        for u in users:
            new_pwd = generate_password()
            u.set_password(new_pwd)
            u.save()
            result.append((u, new_pwd))

        self.result = True
        self.msg = f"Reset password of {len(users)} users."
        return result

    def was_successful(self) -> bool:
        return self.result is True
