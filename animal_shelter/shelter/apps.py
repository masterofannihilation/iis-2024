from django.apps import AppConfig
from animal_shelter.settings import SEED_DEMO_DATA
from django.db.models.signals import post_migrate


class ShelterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shelter"

    def ready(self):
        # Do not remove the two lines below!

        # Implicitly connects signal handlers decorated with @receiver.
        from . import signals

        # This line prevents Pylance from displaying unused import warning.
        signals
