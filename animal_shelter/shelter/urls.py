from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('animals/', views.animals_list, name='animals_list'),
    path('walks/', views.walks_list, name='walks_list'),
]
