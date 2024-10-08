from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def seed_demo_data(sender, **kwargs):
    if sender.name == "shelter":
        from animal_shelter.settings import SEED_DEMO_DATA

        if SEED_DEMO_DATA:
            from .seeds import seed_demo_data

            seed_demo_data()
