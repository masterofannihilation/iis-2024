from typing import Optional
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .actions import ActionOverUsers
from ..models import User
from django.contrib.auth.decorators import login_required
from .list import UserListModel, UserFilterArgs
from django.http.request import HttpRequest
from django.http import HttpResponseForbidden
from django.forms import ModelForm, CheckboxInput, Select, ValidationError
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
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
            self.fields["role"].choices = [(User.Role.VOLUNTEER, User.Role.VOLUNTEER)]

    def clean_role(self):
        role = self.cleaned_data.get("role")

        if self.caregiver and role != User.Role.VOLUNTEER:
            raise ValidationError("Caregivers can only assign the 'Volunteer' role.")

        return role


class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "contact_info"]


def min_user_privileges(
    request: HttpRequest, min_role: User.Role
) -> Optional[HttpResponseForbidden]:
    user: User = request.user  # type: ignore
    if not user.is_authorized_enough(User.Role.CAREGIVER):
        return HttpResponseForbidden("Access Denied: Insufficient privileges.")


# View for users
@login_required
def users_list(request: HttpRequest):
    forbidden = min_user_privileges(request, User.Role.CAREGIVER)
    if forbidden:
        return forbidden

    context = {}

    users = None
    if request.method == "POST":
        context["first_name"] = request.POST.get("first_name", "")
        context["last_name"] = request.POST.get("last_name", "")
        context["email"] = request.POST.get("email", "")
        context["sort_by"] = request.POST.get("sort_by", "")
        if "search" in request.POST or "sort_by" in request.POST:
            fa = UserFilterArgs.from_method_query(request.POST)
            users = UserListModel.search(filter=fa, viewer=request.user)  # type: ignore
        else:
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
                if changed_role_str:
                    changed_role = None
                    try:
                        changed_role = User.Role.from_string(changed_role_str)
                    except ValueError:
                        pass
                    if changed_role:
                        result = action.change_role(changed_role, selected_ids)
            if isinstance(result, HttpResponseForbidden):
                return result
            fa = UserFilterArgs.from_method_query(request.POST)
            users = UserListModel.search(filter=fa, viewer=request.user)  # type: ignore

    if users is None:
        users = UserListModel.search(viewer=request.user)  # type: ignore

    context["users"] = users

    return render(request, "users/list.html", context)


@login_required
def user_detail(request: HttpRequest, id: int):
    forbidden = min_user_privileges(request, User.Role.CAREGIVER)
    if forbidden:
        return forbidden

    user = get_object_or_404(User, id=id)
    return render(request, "users/detail.html", {"user": user, "profile_page": False})


def _user_modification(request: HttpRequest, id: Optional[int], context: dict):
    user = None
    min_role = User.Role.CAREGIVER
    if id:
        user = get_object_or_404(User, id=id)

        min_role = User.Role.ADMINISTRATOR
        if user.role == User.Role.VOLUNTEER:
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
def user_create(request: HttpRequest):
    context = {}

    result = _user_modification(request, None, context)
    if result:
        return result

    return render(request, "users/create.html", context)


@login_required
def user_edit(request: HttpRequest, id: int):
    context = {}

    result = _user_modification(request, id, context)
    if result:
        return result

    return render(request, "users/edit.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


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
    return render(request, "users/detail.html", {"user": user, "profile_page": True})


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
