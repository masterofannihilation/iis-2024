from django.shortcuts import render
from .models import Animal, Walk, VeterinarianRequest, User


# Home page
def home_page(request):
    return render(request, "home.html")


# List all animals
def animals_list(request):
    query = Animal.objects.all()
    name = request.GET.get('name', '')
    species = request.GET.get('species', '')
    if name:
        query = query.filter(name__icontains=name)
    if species:
        query = query.filter(species=species)
    animals = query
    return render(request, "animals/list.html", {"animals": animals})

# View for scheduling walks
def walks_list(request):
    walks = Walk.objects.all()
    return render(request, "walks/list.html", {"walks": walks})
