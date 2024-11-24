from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm, DateTimeInput
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from functools import wraps
from collections import defaultdict
from ..models import Walk, Animal, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.forms.widgets import DateTimeInput
from django import forms

class WalkForm(ModelForm):
    class Meta:
        model = Walk
        fields = ['animal', 'volunteer', 'caregiver', 'begin_time', 'end_time', 'status']
        widgets = {
            'begin_time': DateTimeInput(attrs={'type': 'datetime-local', 'format': '%d.%m.%Y %H:%M'}),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local', 'format': '%d.%m.%Y %H:%M'}),
        }

    begin_time = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'text', 'placeholder': 'dd.mm.YYYY HH:MM'})
    )
    end_time = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'text', 'placeholder': 'dd.mm.YYYY HH:MM'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['status'].initial = Walk.Status.AVAILABLE

    # Custom validation to ensure end_time is after begin_time and no overlapping walks
    def clean(self):
        cleaned_data = super().clean()
        animal = cleaned_data.get("animal")
        begin_time = cleaned_data.get("begin_time")
        end_time = cleaned_data.get("end_time")

        if begin_time and end_time and begin_time >= end_time:
            raise ValidationError({
                'end_time': _("End time must be after begin time.")
            })

        # Check for overlapping walks
        if animal and begin_time and end_time:
            overlapping_walks = Walk.objects.filter(
                animal=animal,
                begin_time__lt=end_time,
                end_time__gt=begin_time
            ).exclude(id=self.instance.id)

            if overlapping_walks.exists():
                raise ValidationError(_("This walk overlaps with another walk for the same animal."))

def user_can_manage_walks(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.role in [User.Role.CAREGIVER, User.Role.ADMINISTRATOR]:
            return HttpResponseForbidden("Access Denied: Insufficient privileges.")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def walks_list(request, id=None):
    if request.method == 'POST':
        walk_id = request.POST.get('walk_id')
        action = request.POST.get('action')
        walk = get_object_or_404(Walk, pk=walk_id)

        if action == 'choose':
            if request.user.role == User.Role.VOLUNTEER and walk.can_be_chosen_by_volunteer():
                walk.volunteer = request.user
                walk.status = Walk.Status.RESERVED
                walk.save()
            else:
                return HttpResponseForbidden("Access Denied: Only volunteers can choose a walk.")
        elif action == 'approve':
            if request.user.role == User.Role.CAREGIVER and walk.can_be_approved_by_caregiver():
                walk.status = Walk.Status.APPROVED
                walk.save()
            else:
                return HttpResponseForbidden("Access Denied: Only caregivers can approve a walk.")

        return redirect('walks_list')

    # Filter walks to include only upcoming walks
    walks = Walk.objects.filter(begin_time__gte=timezone.now())

    # Filter by animal if animal_id is provided
    if id:
        walks = walks.filter(animal_id=id)

    # Apply additional filters if specified
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    species_filter = request.GET.get("species", "")
    status_filter = request.GET.get("status", "")

    if start_date:
        walks = walks.filter(begin_time__date__gte=start_date)
    if end_date:
        walks = walks.filter(begin_time__date__lte=end_date)
    if species_filter:
        walks = walks.filter(animal__species=species_filter)
    if status_filter:
        walks = walks.filter(status=status_filter)

    # Group walks by date (including future dates)
    walks_by_date = defaultdict(list)
    for walk in walks:
        walk_date = walk.begin_time.date()
        walks_by_date[walk_date].append(walk)

    # Convert to a sorted list of tuples (dates will include future dates)
    walks_grouped = sorted(walks_by_date.items())  # List of (date, walks) tuples

    # Species list for filter dropdown
    species_list = Animal.objects.values_list("species", flat=True).distinct()
    status_list = Walk.Status.choices

    return render(
        request,
        "walks/list.html",
        {
            "walks_grouped": walks_grouped,
            "species_list": species_list,
            "status_list": status_list,
            "start_date": start_date,
            "end_date": end_date,
            "species_filter": species_filter,
            "status_filter": status_filter,
            "animal_id": id,
        },
    )

@login_required
@user_can_manage_walks
def walk_create(request):
    if request.method == 'POST':
        form = WalkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('walks_list')
    else:
        form = WalkForm()
    return render(request, 'walks/create.html', {'form': form})

@login_required
def walk_detail(request, walk_id):
    walk = get_object_or_404(Walk, pk=walk_id)
    return render(request, 'walks/detail.html', {'walk': walk})

@login_required
@user_can_manage_walks
def walk_edit(request, walk_id):
    walk = get_object_or_404(Walk, pk=walk_id)
    if request.method == 'POST':
        form = WalkForm(request.POST, instance=walk)
        if form.is_valid():
            form.save()
            return redirect('walks_list')
    else:
        # Format the initial values for display
        initial_data = {
            'begin_time': walk.begin_time.strftime('%d.%m.%Y %H:%M') if walk.begin_time else '',
            'end_time': walk.end_time.strftime('%d.%m.%Y %H:%M') if walk.end_time else '',
        }
        form = WalkForm(instance=walk, initial=initial_data)

    return render(request, 'walks/edit.html', {'form': form})

@login_required
@user_can_manage_walks
def walk_delete(request, walk_id):
    walk = get_object_or_404(Walk, pk=walk_id)
    if request.method == 'POST':
        walk.delete()
        return redirect('walks_list')
    return render(request, 'walks/delete.html', {'walk': walk})

@login_required
def choose_walk(request, walk_id):
    walk = get_object_or_404(Walk, pk=walk_id, status=Walk.Status.AVAILABLE)
    if request.user.role != User.Role.VOLUNTEER:
        return HttpResponseForbidden("Access Denied: Only volunteers can choose a walk.")

    if request.method == 'POST':
        walk.volunteer = request.user
        walk.status = Walk.Status.RESERVED
        walk.save()
        return redirect('walks_list')

    return render(request, 'walks/choose.html', {'walk': walk})

@login_required
def walk_history(request):
    if request.user.role != User.Role.VOLUNTEER:
        return HttpResponseForbidden("Access Denied: Only volunteers can view their walk history.")

    walks = Walk.objects.filter(volunteer=request.user).order_by('-begin_time')
    return render(request, 'walks/history.html', {'walks': walks})
