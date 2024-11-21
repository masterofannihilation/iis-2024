from django.urls import path
from . import views
from .users import views as user_views
from .animals import views as animal_views
from .walks import views as walk_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.home_page, name="home"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", user_views.register, name="register"),
    path("profile/", user_views.profile_detail, name="profile"),
    path("profile/edit/", user_views.profile_edit, name="profile_edit"),
    path(
        "profile/password/", user_views.profile_change_password, name="change_password"
    ),
    path("users/", user_views.users_list, name="users_list"),
    path("users/<int:id>/", user_views.user_detail, name="user_detail"),
    path("users/<int:id>/edit/", user_views.user_edit, name="user_edit"),
    path("users/<int:id>/pwd-reset", user_views.reset_password, name="reset_password"),
    path("users/create/", user_views.user_create, name="user_create"),
    path("animals/", animal_views.animals_list, name="animals_list"),
    path("animals/create/", animal_views.animal_create, name="animal_create"),
    path("animals/<int:id>/", animal_views.animal_detail, name="animal_detail"),
    path("animals/<int:id>/edit/", animal_views.animal_edit, name="animal_edit"),
    path("animals/<int:id>/delete/", animal_views.animal_delete, name="animal_delete"),
    path("walks/", walk_views.walks_list, name="walks_list"),
    path("walks/create/", walk_views.walk_create, name="walk_create"),
    path("walks/<int:walk_id>/", walk_views.walk_detail, name="walk_detail"),
    path("walks/<int:walk_id>/edit/", walk_views.walk_edit, name="walk_edit"),
    path("walks/<int:walk_id>/delete/", walk_views.walk_delete, name="walk_delete"),
]