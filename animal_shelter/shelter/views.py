from django.shortcuts import render
from .models import Animal, Walk, VeterinarianRequest, User


# Home page
def home_page(request):
    return render(request, "home.html")


def animals_list(request):
    animals = Animal.objects.all()

    species_list = Animal.objects.values_list('species', flat=True).distinct()

    name_filter = request.GET.get('name', '')
    species_filter = request.GET.get('species', '')

    if name_filter:
        animals = animals.filter(name__icontains=name_filter)

    if species_filter:
        animals = animals.filter(species=species_filter)

    return render(request, 'animals/list.html', {
        'animals': animals,
        'species_list': species_list
    })


# View for scheduling walks
def walks_list(request):
    walks = Walk.objects.all()
    return render(request, "walks/list.html", {"walks": walks})
