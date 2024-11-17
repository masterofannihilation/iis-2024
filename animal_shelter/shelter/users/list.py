from ..models import User
from typing import Optional
from django.http.request import QueryDict
from django.core.paginator import Paginator, Page


class UserFilterArgs:
    def __init__(self):
        self.username = ""
        self.first_name = ""
        self.last_name: Optional[str] = None
        self.email = ""
        self.role: Optional[User.Role] = None
        self.sort_by: Optional[str] = None
        self.descending = False
        self.page: int = 1

    @staticmethod
    def from_method_query(query: QueryDict) -> "UserFilterArgs":
        fa = UserFilterArgs()
        check = ("username", "first_name", "last_name", "email", "contact")
        for q in check:
            setattr(fa, q, query.get(q, ""))

        fa.role = User.Role.from_string_safe(query.get("filter_role", ""))

        fa.sort_by = query.get("sort_by", None)
        fa.descending = query.get("descending", "0") != "0"

        fa.page = int(query.get("page", "1"))

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
        filter_args: Optional[UserFilterArgs] = None,
        viewer: Optional[User] = None,
        limit=10,
    ) -> tuple[Page, list["UserListModel"]]:
        if filter_args:
            fa = filter_args
        else:
            fa = UserFilterArgs()

        users = User.objects.all()

        if fa.username:
            users = users.filter(username__istartswith=fa.username)
        if fa.first_name:
            users = users.filter(first_name__istartswith=fa.first_name)
        if fa.last_name:
            users = users.filter(last_name__istartswith=fa.last_name)
        if fa.email:
            users = users.filter(email__icontains=fa.email)
        if fa.role:
            users = users.filter(role=fa.role)

        if fa.sort_by:
            sort_param = f"-{fa.sort_by}" if fa.descending else fa.sort_by
            users = users.order_by(sort_param)

        paginator = Paginator(users, limit)
        page_obj = paginator.get_page(fa.page)

        list_models: list[UserListModel] = []
        for u in page_obj:
            list_models.append(UserListModel(u, viewer))

        return (page_obj, list_models)


class TableHeader:
    def __init__(
        self,
        text: str,
        sorting_on=True,
        sort_by: Optional[str] = None,
        last_sort: str = "",
        *args,
        **kwargs,
    ) -> None:
        self.text = text

        if sort_by:
            self.sort_by = sort_by
        else:
            self.sort_by = self.text.lower().replace(" ", "_")

        self.sorting_on = sorting_on

        self.descending_shown = False
        self.active_sorting = False

    @staticmethod
    def default(
        sort_by_query: str = "", descending_query: bool = False
    ) -> list["TableHeader"]:
        headers = [
            TableHeader(text="", sort_by="", sorting_on=False),
            TableHeader(text="Username", last_sort=sort_by_query),
            TableHeader(text="First Name", last_sort=sort_by_query),
            TableHeader(text="Last Name", last_sort=sort_by_query),
            TableHeader(text="Email", last_sort=sort_by_query),
            TableHeader(text="Contact", sorting_on=False),
            TableHeader(text="Role", sorting_on=True, last_sort=sort_by_query),
            TableHeader(text="Active", sorting_on=False),
            TableHeader(text="Actions", sorting_on=False),
        ]

        for h in headers:
            if sort_by_query == h.sort_by:
                h.descending_shown = descending_query
                h.active_sorting = True
                break

        return headers
