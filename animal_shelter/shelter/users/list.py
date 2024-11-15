from ..models import User
from typing import Optional
from django.http.request import QueryDict

class UserFilterArgs:
    def __init__(self):
        self.first_name = ""
        self.last_name: Optional[str] = None
        self.email = ""
        self.contact = ""
        self.sort_by: Optional[str] = None
        self.descending = False

    @staticmethod
    def from_method_query(query: QueryDict) -> 'UserFilterArgs':
        fa = UserFilterArgs()
        check = ("first_name", "last_name", "email", "contact")
        for q in check:
            setattr(fa, q, query.get(q, None))

        fa.sort_by = query.get("sort_by", None)
        
        descending = query.get("descending", 0)
        fa.descending = descending != 0
        
        return fa



class UserListModel:
    def __init__(self, dal_model: User):
        self.id: int = dal_model.id # type: ignore
        self.username = dal_model.username
        self.first_name = dal_model.first_name
        self.last_name = dal_model.last_name
        self.email = dal_model.email
        self.contact = dal_model.contact_info
        self.role = dal_model.role
        self.is_active = dal_model.is_active

    @staticmethod
    def search(filter: UserFilterArgs = UserFilterArgs()) -> list['UserListModel']:
        users = User.objects.all()
        
        if filter.first_name:
            users = users.filter(first_name__icontains=filter.first_name)
        if filter.last_name:
            users = users.filter(last_name__icontains=filter.last_name)
        if filter.email:
            users = users.filter(email_name__icontains=filter.email)
        if filter.contact:
            users = users.filter(contact__icontains=filter.contact)
        
        list_models: list[UserListModel] = []
        for u in users:
            list_models.append(UserListModel(u))

        return list_models

