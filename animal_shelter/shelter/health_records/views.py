from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm, DateTimeInput, forms
from functools import wraps
from ..models import VeterinarianRequest, Animal, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Case, When, IntegerField
from django.utils import timezone

class HealthRecordCaregiverForm(ModelForm):
    class Meta:
        model = VeterinarianRequest
        fields = ["animal", "veterinarian", "status", "description"]

class HealthRecordVetForm(ModelForm):
    class Meta:
        model = VeterinarianRequest
        fields = ["status", "examination_date", "result"]
        widgets = {
            "examination_date": DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_examination_date(self):
        examination_date = self.cleaned_data.get("examination_date")
        if examination_date and examination_date < timezone.now():
            raise forms.ValidationError("Examination date must be either today or in the future.")
        return examination_date
    
def user_can_create_request(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.role in [User.Role.CAREGIVER]:
            return HttpResponseForbidden("Access Denied: Insufficient privileges.")
        return view_func(request, *args, **kwargs)
    return wrapper

def user_can_manage_request(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.role in [User.Role.CAREGIVER, User.Role.VETERINARIAN]:
            return HttpResponseForbidden("Access Denied: Insufficient privileges.")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def health_records_list(request):
    animals = Animal.objects.all()
    species_list = Animal.AnimalType.choices
    return render(
        request, 
        "health_records/list.html", 
        {
            "animals": animals,
            "species_list": [species[0] for species in species_list]
        }
    )

@login_required
@user_can_create_request
def health_records_create(request):
    if request.method == "POST":
        form = HealthRecordCaregiverForm(request.POST)
        if form.is_valid():
            health_record = form.save(commit=False)
            health_record.caregiver = request.user
            health_record.save()
            return redirect("health_records_detail", id=health_record.animal.id)
    else:
        form = HealthRecordCaregiverForm()
    return render(request, "health_records/create.html", {"form": form})

@login_required
@user_can_manage_request
def health_records_caregiver_edit(request, id):
    health_record = get_object_or_404(VeterinarianRequest, id=id)
    if request.method == "POST":
        form = HealthRecordCaregiverForm(request.POST, instance=health_record)
        if form.is_valid():
            form.save()
            return redirect("health_records_detail", id=health_record.animal.id)
    else:
        form = HealthRecordCaregiverForm(instance=health_record)
    return render(request, "health_records/edit.html", {"form": form})

@login_required
@user_can_manage_request
def health_records_vet_edit(request, id):
    health_record = get_object_or_404(VeterinarianRequest, id=id)
    if request.method == "POST":
        form = HealthRecordVetForm(request.POST, instance=health_record)
        if form.is_valid():
            form.save()
            return redirect("health_records_detail", id=health_record.animal.id)
    else:
        form = HealthRecordVetForm(instance=health_record)
    return render(request, "health_records/edit_vet.html", {"form": form})

@login_required
def health_records_detail(request, id):
    animal = get_object_or_404(Animal, id=id)
    health_records = VeterinarianRequest.objects.filter(animal=animal).annotate(
        # Order requests by status
        status_order=Case(
            When(status=VeterinarianRequest.Status.REQUESTED, then=0),
            When(status=VeterinarianRequest.Status.SCHEDULED, then=1),
            When(status=VeterinarianRequest.Status.COMPLETED, then=2),
            output_field=IntegerField(),
        )
    ).order_by('status_order')
    return render(request, "health_records/detail.html", {"animal": animal, "health_records": health_records})

@login_required
@user_can_manage_request
def health_records_delete(request, id):
    record = get_object_or_404(VeterinarianRequest, id=id)
    if request.method == "POST":
        record.delete()
        return redirect("health_records_detail", id=record.animal.id)
    return render(request, "health_records/delete.html", {"health_record": record})

@login_required
def choose_health_record(request, id):
    health_record = get_object_or_404(VeterinarianRequest, pk=id, veterinarian__isnull=True)
    if request.user.role != User.Role.VETERINARIAN:
        return HttpResponseForbidden("Access Denied: Only veterinarians can choose a health record.")
    
    if request.method == 'POST':
        if health_record.veterinarian is None:
            health_record.veterinarian = request.user
            # health_record.status = VeterinarianRequest.Status.SCHEDULED
            health_record.save()
        return redirect('health_records_detail', id=health_record.animal.id)
    
    return redirect('health_records_detail', id=health_record.animal.id)
