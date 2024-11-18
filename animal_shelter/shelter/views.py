from django.shortcuts import render
from .models import Animal, Walk, VeterinarianRequest, User


# Home page
def home_page(request):
    return render(request, "home.html")


# View for scheduling walks
def walks_list(request):
    walks = Walk.objects.all()
    return render(request, "walks/list.html", {"walks": walks})
