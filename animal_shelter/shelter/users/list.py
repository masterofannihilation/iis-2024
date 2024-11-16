from ..models import User
from typing import Optional
from django.http.request import QueryDict


class UserFilterArgs:
    def __init__(self):
        self.first_name = ""
        self.last_name: Optional[str] = None
        self.email = ""
        self.sort_by: Optional[str] = None
        self.descending = False

    @staticmethod
    def from_method_query(query: QueryDict) -> "UserFilterArgs":
        fa = UserFilterArgs()
        check = ("first_name", "last_name", "email", "contact")
        for q in check:
            setattr(fa, q, query.get(q, None))

        fa.sort_by = query.get("sort_by", None)
        if fa.sort_by:
            if fa.sort_by.startswith("DESCENDING_"):
                fa.descending = True
                fa.sort_by = fa.sort_by[len("DESCENDING_") :]

        return fa


class UserListModel:
    def __init__(self, dal_model: User, viewer: Optional[User] = None):
        self.id: int = dal_model.id  # type: ignore
        self.username = dal_model.username
        self.first_name = dal_model.first_name
        self.last_name = dal_model.last_name
        self.email = dal_model.email
        self.contact = dal_model.contact_info
        self.role = dal_model.role
        self.is_active = dal_model.is_active
        self.modifiable = False

        if viewer:
            if viewer == dal_model:
                self.modifiable = False
            elif viewer.role == User.Role.ADMINISTRATOR:
                self.modifiable = True
            elif (
                viewer.role == User.Role.CAREGIVER and self.role == User.Role.VOLUNTEER
            ):
                self.modifiable = True

    @staticmethod
    def search(
        filter: UserFilterArgs = UserFilterArgs(), viewer: Optional[User] = None
    ) -> list["UserListModel"]:
        users = User.objects.all()

        if filter.first_name:
            users = users.filter(first_name__icontains=filter.first_name)
        if filter.last_name:
            users = users.filter(last_name__icontains=filter.last_name)
        if filter.email:
            users = users.filter(email__icontains=filter.email)

        if filter.sort_by:
            users = users.order_by(filter.sort_by)

        list_models: list[UserListModel] = []
        for u in users:
            list_models.append(UserListModel(u, viewer))

        if filter.descending:
            list_models.reverse()

        return list_models
