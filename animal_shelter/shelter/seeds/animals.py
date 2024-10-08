from ..models import Animal
import datetime

ANIMAL_SEEDS = (
    Animal(
        id=1_000_000,
        name="Rex",
        species="Dog",
        date_of_birth=datetime.datetime(2019, 1, 1),
        description="Former police dog",
        intake_date=datetime.datetime.now(),
    ),
)
