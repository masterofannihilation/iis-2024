from django.urls import path
from . import views

urlpatterns = [
    path('animals/', views.animal_list, name='animal_list'),
    path('walks/', views.walk_schedule, name='walk_schedule'),
]
