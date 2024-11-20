from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm, DateInput
from functools import wraps
from ..models import Animal, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import requests
from urllib.parse import urlparse

class AnimalForm(ModelForm):
    class Meta:
        model = Animal
        fields = ["name", "species", "date_of_birth", "description", "intake_date", "image_url"]
        widgets = {
            "date_of_birth": DateInput(attrs={"type": "date"}),
            "intake_date": DateInput(attrs={"type": "date"}),
        }

def is_valid_image_url(url):
    if not url:
        return False

    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return False

    try:
        response = requests.get(url, timeout=2)
        if response.status_code != 200:
            return False

        # Check if the content type is an image
        content_type = response.headers.get('Content-Type')
        if content_type and content_type.startswith('image/'):
            return True
        else:
            return False

    except requests.RequestException as e:
        return False, f"Error: {str(e)}"


def user_can_manage_animals(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.role in [User.Role.CAREGIVER, User.Role.ADMINISTRATOR]:
            return HttpResponseForbidden("Access Denied: Insufficient privileges.")
        return view_func(request, *args, **kwargs)

    return wrapper

def animal_detail(request, id):
    animal = get_object_or_404(Animal, id=id)
    return render(request, "animals/detail.html", {"animal": animal})

def animals_list(request):
    animals = Animal.objects.all()

    species_list = Animal.objects.values_list("species", flat=True).distinct()

    name_filter = request.GET.get("name", "")
    species_filter = request.GET.get("species", "")

    if name_filter:
        animals = animals.filter(name__icontains=name_filter)

    if species_filter:
        animals = animals.filter(species=species_filter)

    return render(
        request, "animals/list.html", {"animals": animals, "species_list": species_list}
    )


@login_required
@user_can_manage_animals
def animal_create(request):
    available_species = [species[0] for species in Animal.AnimalType.choices]
    if request.method == "POST":
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            if not is_valid_image_url(animal.image_url):
                animal.image_url = ""
            animal.save()
            return redirect("animal_detail", id=animal.id)
    else:
        form = AnimalForm()
    return render(request, "animals/create.html", {"form": form, "available_species": available_species})



@login_required
@user_can_manage_animals
def animal_edit(request, id):
    animal = get_object_or_404(Animal, id=id)
    available_species = [species[0] for species in Animal.AnimalType.choices]

    if request.method == "POST":
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            animal = form.save(commit=False)
            if not is_valid_image_url(animal.image_url):
                animal.image_url = ""
            animal.save()
            return redirect("animal_detail", id=animal.id)
    else:
        form = AnimalForm(instance=animal)
    return render(request, "animals/edit.html", {"form": form, "animal": animal, "available_species": available_species})


@login_required
@user_can_manage_animals
def animal_delete(request, id):
    animal = get_object_or_404(Animal, id=id)
    if request.method == "POST":
        animal.delete()
        return redirect("animals_list")
    return render(request, "animals/delete.html", {"animal": animal})
