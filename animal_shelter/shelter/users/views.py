from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from ..models import User
from django.contrib.auth.decorators import login_required
from .list import UserListModel, UserFilterArgs
from django.http.request import HttpRequest
from django.http import HttpResponseForbidden
from django.forms import ModelForm, CheckboxInput, Select
from django.contrib.auth import logout


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


class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "contact_info"]


# View for users
@login_required
def users_list(request: HttpRequest):
    if request.user.role != User.Role.ADMINISTRATOR:  # type: ignore
        return HttpResponseForbidden(
            "Access Denied: Insufficient privileges."
        )

    context = {}

    users = None
    if request.method == "POST":
        context["first_name"] = request.POST.get("first_name", "")
        context["last_name"] = request.POST.get("last_name", "")
        context["email"] = request.POST.get("email", "")
        context["contact"] = request.POST.get("contact", "")
        if "search" in request.POST:
            fa = UserFilterArgs.from_method_query(request.POST)
            users = UserListModel.search(filter=fa)

    if users is None:
        users = UserListModel.search()

    context["users"] = users

    return render(request, "users/list.html", context)


@login_required
def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, "users/detail.html", {"user": user, "profile_page": False})


@login_required
def user_create(request):
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            saved_user: User = form.save()
            return redirect("user_detail", id=saved_user.id)  # type: ignore
    else:
        form = UserEditForm()

    return render(request, "users/create.html", {"form": form})


@login_required
def user_edit(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_detail", id=id)
    else:
        form = UserEditForm(instance=user)

    return render(request, "users/edit.html", {"form": form, "user": user})


def logout_view(request):
    logout(request)
    return redirect("login")


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
            return redirect("user_detail", id=id)
    else:
        form = ProfileEditForm(instance=user)

    return render(request, "users/edit.html", {"form": form, "user": user})
