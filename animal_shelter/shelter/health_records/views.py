from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm, DateTimeInput, ModelChoiceField, Select, forms
from functools import wraps
from ..models import VeterinarianRequest, Animal, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Case, When, IntegerField
from django.utils import timezone

class HealthRecordCaregiverForm(ModelForm):
    veterinarian = ModelChoiceField(
        queryset=User.objects.filter(role=User.Role.VETERINARIAN),
        required=False,
        widget=Select,
        label="Veterinarian",
    )
    class Meta:
        model = VeterinarianRequest
        fields = ["veterinarian", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veterinarian'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name} ({obj.username})"

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
@user_can_create_request
def health_records_create(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    if request.method == "POST":
        form = HealthRecordCaregiverForm(request.POST)
        if form.is_valid():
            health_record = form.save(commit=False)
            health_record.status = VeterinarianRequest.Status.REQUESTED
            health_record.request_date = timezone.now()
            health_record.caregiver = request.user
            health_record.animal = animal
            health_record.save()
            return redirect("health_records_detail", id=animal.id)
    else:
        form = HealthRecordCaregiverForm()
    return render(request, "health_records/create.html", {"form": form, "animal": animal})

@login_required
@user_can_create_request
def health_records_caregiver_edit(request, animal_id, id):
    health_record = get_object_or_404(VeterinarianRequest, id=id, animal_id=animal_id)
    # Check if the status is REQUESTED
    if health_record.status != VeterinarianRequest.Status.REQUESTED or health_record.caregiver != request.user:
        return HttpResponseForbidden("Access Denied: Only requests with status 'REQUESTED' can be edited by caregivers.")
    if request.method == "POST":
        form = HealthRecordCaregiverForm(request.POST, instance=health_record)
        if form.is_valid():
            form.save()
            return redirect("health_records_detail", id=animal_id)
    else:
        form = HealthRecordCaregiverForm(instance=health_record)
    return render(request, "health_records/edit.html", {"form": form, "animal_id": animal_id})

@login_required
@user_can_manage_request
def health_records_vet_edit(request, animal_id, id):
    health_record = get_object_or_404(VeterinarianRequest, id=id, animal_id=animal_id)
    if request.method == "POST":
        form = HealthRecordVetForm(request.POST, instance=health_record)
        if form.is_valid() and health_record.examination_date is not None:
            health_record.save()
            return redirect("health_records_detail", id=animal_id)
        else:
            # If form is invalid keep old data
            form = HealthRecordVetForm(instance=health_record)
            return redirect("health_records_detail", id=animal_id)
    else:
        form = HealthRecordVetForm(instance=health_record)
    return render(request, "health_records/edit_vet.html", {"form": form, "animal_id": animal_id})

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
def health_records_delete(request, animal_id, id):
    record = get_object_or_404(VeterinarianRequest, id=id, animal_id=animal_id)
    if request.method == "POST":
        record.delete()
        return redirect("health_records_detail", id=animal_id)
    return render(request, "health_records/delete.html", {"health_record": record, "animal_id": animal_id})

@login_required
def choose_health_record(request, animal_id, id):
    health_record = get_object_or_404(VeterinarianRequest, pk=id, veterinarian__isnull=True, animal_id=animal_id)
    if request.user.role != User.Role.VETERINARIAN:
        return HttpResponseForbidden("Access Denied: Only veterinarians can choose a health record.")
    
    if request.method == 'POST':
        if health_record.veterinarian is None:
            health_record.veterinarian = request.user
            health_record.save()
        return redirect('health_records_detail', id=animal_id)
    
    return redirect('health_records_detail', id=animal_id)