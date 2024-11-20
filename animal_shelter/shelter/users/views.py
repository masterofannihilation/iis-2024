from functools import wraps
from typing import Optional
from django.shortcuts import render, redirect, get_object_or_404
from .actions import ActionOverUsers
from ..models import User
from django.contrib.auth.decorators import login_required
from .list import TableHeader, UserListModel, UserFilterArgs
from django.http.request import HttpRequest
from django.http import HttpResponseForbidden, QueryDict
from django.forms import (
    ModelForm,
    CheckboxInput,
    Select,
    ValidationError,
    EmailField,
    CharField,
    Textarea,
    TextInput,
    PasswordInput,
    EmailInput,
)
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "role",
            "contact_info",
        ]
        widgets = {
            "role": Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        self.caregiver = kwargs.pop("caregiver", None)
        super().__init__(*args, **kwargs)
        if self.caregiver:
            self.fields["role"].choices = [
                (User.Role.VOLUNTEER, User.Role.VOLUNTEER),
                (User.Role.UNVERIFIED, User.Role.UNVERIFIED),
            ]

    def clean_role(self):
        role = self.cleaned_data.get("role")

        if self.caregiver and role not in (User.Role.VOLUNTEER, User.Role.UNVERIFIED):
            raise ValidationError("Caregivers can only assign the 'Volunteer' role.")

        return role


class CustomRegistrationForm(UserCreationForm):
    username = CharField(
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
        label_suffix="*",
    )
    password1 = CharField(
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"}),
        label="Password",
        label_suffix="*",
    )
    password2 = CharField(
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"}),
        label="Repeat password",
        label_suffix="*",
    )
    email = EmailField(
        required=False, widget=EmailInput(attrs={"class": "form-control"})
    )

    contact_info = CharField(
        required=False, widget=Textarea(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "first_name",
            "last_name",
            "contact_info",
        ]


class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "contact_info"]


def user_can_manage_users(view_func):
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        user: Optional[User] = request.user if request.user.is_authenticated else None  # type: ignore
        forbid_access = not request.user.is_authenticated

        if user:
            forbid_access = not user.role in [
                User.Role.CAREGIVER,
                User.Role.ADMINISTRATOR,
            ]
        else:
            forbid_access = True

        if forbid_access:
            return HttpResponseForbidden("Access Denied: Insufficient privileges.")

        return view_func(request, *args, **kwargs)

    return wrapper


def _copy_query_params(query: QueryDict, exclude: list[str] = []) -> QueryDict:
    copied = query.copy()
    copied._mutable = True
    for q in exclude:
        copied.pop(q, "")
    return copied


def min_user_privileges(
    request: HttpRequest, min_role: User.Role
) -> Optional[HttpResponseForbidden]:
    user: User = request.user  # type: ignore
    if not user.is_authorized_enough(min_role):
        return HttpResponseForbidden("Access Denied: Insufficient privileges.")


@login_required
@user_can_manage_users
def users_list(request: HttpRequest):
    context = {}

    context["is_admin"] = request.user.role == User.Role.ADMINISTRATOR  # type: ignore

    users_page = None
    sort_by_query = ""
    last_descending = False
    if request.method == "POST":
        selected_users = request.POST.getlist("selected_users")
        selected_ids = list(map(int, selected_users))
        action = ActionOverUsers(request.user)  # type: ignore
        result = None
        if "activate" in request.POST:
            result = action.set_active_state(True, selected_ids)
        elif "deactivate" in request.POST:
            result = action.set_active_state(False, selected_ids)
        elif "delete" in request.POST:
            result = action.delete(selected_ids)
        elif "change_role":
            changed_role_str = request.POST.get("role")
            action.result = False
            action.msg = f"No role was chosen!"
            if changed_role_str:
                changed_role = None
                try:
                    changed_role = User.Role.from_string(changed_role_str)
                except ValueError:
                    pass
                if changed_role is not None:
                    result = action.change_role(changed_role, selected_ids)
        if action.was_successful():
            messages.success(request, action.msg)
        else:
            if isinstance(action.result, HttpResponseForbidden):
                messages.error(request, str(action.result.content))
            else:
                messages.error(request, action.msg)
        users_page = UserListModel.search(viewer=request.user)  # type: ignore
    else:  # GET method
        fa = UserFilterArgs.from_method_query(request.GET)
        users_page = UserListModel.search(filter_args=fa, viewer=request.user)  # type: ignore
        sort_by_query = fa.sort_by if fa.sort_by else ""
        last_descending = request.GET.get("descending", "0") != "0"

        context["filters_page"] = _copy_query_params(request.GET, ["page"])
        context["filters_sort"] = _copy_query_params(
            request.GET, ["sort_by", "descending"]
        )

    context["page_obj"] = users_page[0]
    context["users"] = users_page[1]

    context["headers"] = TableHeader.default(sort_by_query, last_descending)

    return render(request, "users/list.html", context)


@login_required
@user_can_manage_users
def user_detail(request: HttpRequest, id: int):
    user = get_object_or_404(User, id=id)
    return render(request, "users/detail.html", {"user": UserListModel(user, viewer=request.user), "profile_page": False})  # type: ignore


def _user_modification(request: HttpRequest, id: Optional[int], context: dict):
    user = None
    min_role = User.Role.CAREGIVER
    if id:
        user = get_object_or_404(User, id=id)

        min_role = User.Role.ADMINISTRATOR
        if user.role in (User.Role.VOLUNTEER, User.Role.UNVERIFIED):
            min_role = User.Role.CAREGIVER
    forbidden = min_user_privileges(request, min_role)
    if forbidden:
        return forbidden

    caregiver_logged_in = request.user.role == User.Role.CAREGIVER  # type: ignore

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user, caregiver=caregiver_logged_in)
        if form.is_valid():
            saved_user = form.save()
            return redirect("user_detail", id=saved_user.id)
    else:
        form = UserEditForm(instance=user, caregiver=caregiver_logged_in)

    context["form"] = form
    context["user"] = user


@login_required
@user_can_manage_users
def user_create(request: HttpRequest):
    context = {}

    result = _user_modification(request, None, context)
    if result:
        return result

    return render(request, "users/create.html", context)


@login_required
@user_can_manage_users
def user_edit(request: HttpRequest, id: int):
    context = {}

    result = _user_modification(request, id, context)
    if result:
        return result

    return render(request, "users/edit.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


def register(request: HttpRequest):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "You have successfully registered! Contact caregivers to verify you as a volunteer.",
            )
            return redirect("login")  # Replace 'login' with the name of your login view
    else:
        form = CustomRegistrationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def reset_password(request: HttpRequest, id: int):
    user = get_object_or_404(User, id=id)  # type: ignore

    action = ActionOverUsers(requested_by=request.user)  # type: ignore
    result = action.reset_password([id])
    if isinstance(result, HttpResponseForbidden):
        return result

    new_pwd = result[0][1]
    messages.success(
        request,
        f"New password has been sent to the user via email. (secret - new password: {new_pwd})",
    )
    return redirect("user_detail", id=id)


@login_required
def profile_detail(request: HttpRequest):
    user = get_object_or_404(User, id=request.user.id)  # type: ignore
    return render(
        request,
        "users/detail.html",
        {"user": UserListModel(user), "profile_page": True},
    )


@login_required
def profile_edit(request: HttpRequest):
    user = get_object_or_404(User, id=request.user.id)  # type: ignore

    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=user)

    return render(request, "users/edit.html", {"form": form, "user": user})


@login_required
def profile_change_password(request: HttpRequest):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)  # type: ignore
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # prevent logout
            messages.success(request, "Your password has been changed successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(user=request.user)  # type: ignore

    return render(request, "users/password.html", {"form": form})
