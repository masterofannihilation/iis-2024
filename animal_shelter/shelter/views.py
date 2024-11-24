from django.http import HttpRequest
from django.shortcuts import render
from .models import Animal, Walk, VeterinarianRequest, User
from django import forms
import random


# Home page
def home_page(request):
    animals = Animal.objects.all()
    random_animals = random.sample(list(animals), min(len(animals) - 1, 15))
    valid_animals = [animal for animal in random_animals if animal.image_url]
    return render(request, "home.html", {"animals": valid_animals})


def about_page(request: HttpRequest):
    return render(request, "about.html")


# View for scheduling walks
def walks_list(request):
    walks = Walk.objects.all()
    return render(request, "walks/list.html", {"walks": walks})
