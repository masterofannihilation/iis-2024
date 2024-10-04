from django.contrib import admin
from .models import User, Animal, Walk, VeterinarianRequest

admin.site.register(User)
admin.site.register(Animal)
admin.site.register(Walk)
admin.site.register(VeterinarianRequest)
