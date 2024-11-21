import datetime
import pytz
from ..models import Walk

WALK_SEEDS = (
    Walk(
        id=1_003_000,
        animal_id=1_002_000,  # Rex
        volunteer_id=1_001_008,  # Willow Jones
        caregiver_id=1_001_002,  # Tamara Pollar
        begin_time=datetime.datetime(2023, 11, 2, 10, 0, tzinfo=pytz.UTC),  # Include time and timezone
        end_time=datetime.datetime(2023, 11, 2, 12, 0, tzinfo=pytz.UTC),  # Include time and timezone
        status=Walk.Status.RETURNED,
    ),
    Walk(
        id=1_003_001,
        animal_id=1_002_001,  # Jambo
        volunteer_id=1_001_012,  # Althea Hays
        caregiver_id=1_001_003,  # Upton Harvey
        begin_time=datetime.datetime(2023, 10, 21, 9, 0, tzinfo=pytz.UTC),  # Include time and timezone
        end_time=datetime.datetime(2023, 10, 21, 11, 0, tzinfo=pytz.UTC),  # Include time and timezone
        status=Walk.Status.BORROWED,
        ),
    Walk(
        id=1_003_002,
        animal_id=1_002_002,  # Hopper
        volunteer_id=1_001_008,  # Ignatius Lowery
        caregiver_id=1_001_006,  # Evelyn Zimmerman
        begin_time=datetime.datetime(2023, 9, 16, 8, 0, tzinfo=pytz.UTC),  # Include time and timezone
        end_time=datetime.datetime(2023, 9, 16, 10, 0, tzinfo=pytz.UTC),  # Include time and timezone
        status=Walk.Status.RETURNED,
    ),
    Walk(
        id=1_003_003,
        animal_id=1_002_003,  # Shadow
        volunteer_id=1_001_020,  # Randall Deleon
        caregiver_id=1_001_010,  # Nayda Moses
        begin_time=datetime.datetime(2023, 8, 11, 7, 0, tzinfo=pytz.UTC),  # Include time and timezone
        end_time=datetime.datetime(2023, 8, 11, 9, 0, tzinfo=pytz.UTC),  # Include time and timezone
        status=Walk.Status.BORROWED,
    ),
    Walk(
        id=1_003_004,
        animal_id=1_002_004,  # Mittens
        volunteer_id=1_001_008,  # Catherine Logan
        caregiver_id=1_001_014,  # Priscilla Barnes
        begin_time=datetime.datetime(2023, 7, 6, 6, 0, tzinfo=pytz.UTC),  # Include time and timezone
        end_time=datetime.datetime(2023, 7, 6, 8, 0, tzinfo=pytz.UTC),  # Include time and timezone
        status=Walk.Status.RETURNED,
    ),
    Walk(
        id=1_003_005,
        animal_id=1_002_005,  # Bunny
        volunteer_id=1_001_018,  # Tucker Webster
        caregiver_id=1_001_022,  # Amity Dudley
        begin_time=datetime.datetime(2023, 6, 19, 5, 0, tzinfo=pytz.UTC),  # Include time and timezone
        end_time=datetime.datetime(2023, 6, 19, 7, 0, tzinfo=pytz.UTC),  # Include time and timezone
        status=Walk.Status.BORROWED,
    ),
    Walk(
        id=1_003_006,
        animal_id=1_002_006,  # Patches
        volunteer_id=1_001_025,  # John Doe
        caregiver_id=1_001_004,  # Rae Blake
        begin_time=datetime.datetime(2023, 5, 26, 4, 0, tzinfo=pytz.UTC),  # Include time and timezone
        end_time=datetime.datetime(2023, 5, 26, 6, 0, tzinfo=pytz.UTC),  # Include time and timezone
        status=Walk.Status.RETURNED,
    ),
    Walk(
        id=1_003_007,
        animal_id=1_002_007,  # Bolt
        volunteer_id=1_001_023,  # Beck Reeves
        caregiver_id=1_001_019,  # Neil Fox
        begin_time=datetime.datetime(2023, 4, 11, 3, 0, tzinfo=pytz.UTC),  # Include time and timezone
        end_time=datetime.datetime(2023, 4, 11, 5, 0, tzinfo=pytz.UTC),  # Include time and timezone
        status=Walk.Status.BORROWED,
    ),
     Walk(
        id=1_003_008,
        animal_id=1_002_000,  # Rex
        volunteer_id=None,  # No volunteer assigned
        caregiver_id=1_001_002,  # Tamara Pollar
        begin_time=datetime.datetime(2023, 12, 2, 10, 0, tzinfo=pytz.UTC),  # Future date
        end_time=datetime.datetime(2023, 12, 2, 12, 0, tzinfo=pytz.UTC),  # Future date
        status=Walk.Status.AVAILABLE,
    ),
    Walk(
        id=1_003_009,
        animal_id=1_002_001,  # Jambo
        volunteer_id=None,  # No volunteer assigned
        caregiver_id=1_001_003,  # Upton Harvey
        begin_time=datetime.datetime(2023, 12, 3, 9, 0, tzinfo=pytz.UTC),  # Future date
        end_time=datetime.datetime(2023, 12, 3, 11, 0, tzinfo=pytz.UTC),  # Future date
        status=Walk.Status.AVAILABLE,
    ),   
    
)