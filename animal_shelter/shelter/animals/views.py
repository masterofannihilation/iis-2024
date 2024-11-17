from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm, DateInput
from functools import wraps
from ..models import Animal, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

class AnimalForm(ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'species', 'date_of_birth', 'description', 'intake_date']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'intake_date': DateInput(attrs={'type': 'date'}),
        }


def user_can_manage_animals(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.role in [User.Role.CAREGIVER, User.Role.ADMINISTRATOR]:
            return HttpResponseForbidden("Access Denied: Insufficient privileges.")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@user_can_manage_animals
def animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('animals_list')

    else:
        form = AnimalForm()
    return render(request, 'animals/create.html', {'form': form})


@login_required
def animal_detail(request, id):
    animal = get_object_or_404(Animal, id=id)
    return render(request, 'animals/detail.html', {'animal': animal})


@login_required
@user_can_manage_animals
def animal_edit(request, id):
    animal = get_object_or_404(Animal, id=id)
    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('animal_detail', id=id)
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'animals/edit.html', {'form': form, 'animal': animal})


@login_required
@user_can_manage_animals
def animal_delete(request, id):
    animal = get_object_or_404(Animal, id=id)
    if request.method == 'POST':
        animal.delete()
        return redirect('animals_list')
    return render(request, 'animals/delete.html', {'animal': animal})
