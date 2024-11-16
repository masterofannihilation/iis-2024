from django.urls import path
from . import views
from .users import views as user_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home_page, name='home'),
    path('animals/', views.animals_list, name='animals_list'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('profile/', user_views.profile_detail, name='profile'),
    path('profile/edit/', user_views.profile_edit, name='profile_edit'),
    path('profile/password/', user_views.profile_change_password, name='change_password'),
    path('users/', user_views.users_list, name='users_list'),
    path('users/<int:id>/', user_views.user_detail, name='user_detail'),
    path('users/<int:id>/edit/', user_views.user_edit, name='user_edit'),
    path('users/<int:id>/pwd-reset', user_views.reset_password, name='reset_password'),
    path('users/create/', user_views.user_create, name='user_create'),
    path('walks/', views.walks_list, name='walks_list'),
]
