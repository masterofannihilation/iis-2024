from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelForm, DateInput
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from functools import wraps
from collections import defaultdict
from ..models import Walk, Animal, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


class WalkForm(ModelForm):
    class Meta:
        model = Walk
        fields = ['animal', 'volunteer', 'caregiver', 'begin_time', 'end_time', 'status']
        widgets = {
            'begin_time': DateInput(attrs={'type': 'date'}),
            'end_time': DateInput(attrs={'type': 'date'}),
        }
    
    # Custom validation to ensure end_time is after begin_time
    def clean(self):
        cleaned_data = super().clean()
        begin_time = cleaned_data.get("begin_time")
        end_time = cleaned_data.get("end_time")

        if begin_time and end_time and begin_time >= end_time:
            raise ValidationError({
                'end_time': _("End time must be after begin time.")
            })

def user_can_manage_walks(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.role in [User.Role.CAREGIVER, User.Role.ADMINISTRATOR]:
            return HttpResponseForbidden("Access Denied: Insufficient privileges.")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def walks_list(request):
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
    
    walks = Walk.objects.all()

    # Apply filters only if specified
    time_filter = request.GET.get("time", "")
    species_filter = request.GET.get("species", "")
    status_filter = request.GET.get("status", "")

    if time_filter:
        walks = walks.filter(begin_time__date=time_filter)  # Matches specific date
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
            "time_filter": time_filter,
            "species_filter": species_filter,
            "status_filter": status_filter,
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
        form = WalkForm(instance=walk)
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