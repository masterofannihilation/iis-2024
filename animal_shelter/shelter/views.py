from django.shortcuts import render
from .models import Animal, Walk, VeterinarianRequest, User


# Home page
def home_page(request):
    return render(request, "home.html")


# List all animals
def animals_list(request):
    animals = Animal.objects.all()
    return render(request, "animals/list.html", {"animals": animals})

# View for scheduling walks
def walks_list(request):
    walks = Walk.objects.all()
    return render(request, "walks/list.html", {"walks": walks})
