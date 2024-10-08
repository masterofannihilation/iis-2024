from ..models import User, Animal, Walk, VeterinarianRequest


def seed_demo_data():
    tables = (User, Animal, Walk, VeterinarianRequest)
    for table in tables:
        table.objects.all().delete()

    from .animals import ANIMAL_SEEDS

    seeds = (ANIMAL_SEEDS,)
    for data in seeds:
        for entry in data:
            entry.save()
