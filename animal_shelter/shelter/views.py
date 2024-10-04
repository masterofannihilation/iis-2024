from django.shortcuts import render
from .models import Animal, Walk, VeterinarianRequest

# List all animals
def animal_list(request):
    animals = Animal.objects.all()
    return render(request, 'shelter/animal_list.html', {'animals': animals})

# View for scheduling walks
def walk_schedule(request):
    walks = Walk.objects.all()
    return render(request, 'shelter/walk_schedule.html', {'walks': walks})
