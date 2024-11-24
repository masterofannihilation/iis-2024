from ..models import VeterinarianRequest
import datetime
import pytz

HEALTH_RECORD_SEEDS = (
    VeterinarianRequest(
        id=1_003_000,
        animal_id=1_002_000,
        caregiver_id=1_001_002,
        veterinarian_id=1_001_004,
        request_date=datetime.date(2023, 11, 5),
        status=VeterinarianRequest.Status.REQUESTED,
        examination_date=None,
        result=None,
    ),
    VeterinarianRequest(
        id=1_003_001,
        animal_id=1_002_001,
        caregiver_id=1_001_003,
        veterinarian_id=1_001_007,
        request_date=datetime.date(2023, 10, 25),
        status=VeterinarianRequest.Status.SCHEDULED,
        examination_date=datetime.datetime(2023, 11, 10, 0, 0, tzinfo=pytz.UTC),
        result=None,
    ),
    VeterinarianRequest(
        id=1_003_002,
        animal_id=1_002_001,
        caregiver_id=1_001_006,
        veterinarian_id=1_001_011,
        request_date=datetime.date(2023, 9, 20),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 10, 1, 0, 0, tzinfo=pytz.UTC),
        result="Healthy, no issues found.",
    ),
    VeterinarianRequest(
        id=1_003_003,
        animal_id=1_002_003,
        caregiver_id=1_001_010,
        veterinarian_id=1_001_015,
        request_date=datetime.date(2023, 8, 15),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 8, 25, 0, 0, tzinfo=pytz.UTC),
        result="Minor skin infection treated.",
    ),
    VeterinarianRequest(
        id=1_003_004,
        animal_id=1_002_004,
        caregiver_id=1_001_014,
        veterinarian_id=1_001_019,
        request_date=datetime.date(2023, 7, 10),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 7, 20, 0, 0, tzinfo=pytz.UTC),
        result="Vaccinated and dewormed.",
    ),
    VeterinarianRequest(
        id=1_003_005,
        animal_id=1_002_005,
        caregiver_id=1_001_018,
        veterinarian_id=1_001_023,
        request_date=datetime.date(2023, 6, 20),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 6, 30, 0, 0, tzinfo=pytz.UTC),
        result="Dental check-up completed.",
    ),
    VeterinarianRequest(
        id=1_003_006,
        animal_id=1_002_006,
        caregiver_id=1_001_002,
        veterinarian_id=1_001_004,
        request_date=datetime.date(2023, 5, 30),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 6, 10, 0, 0, tzinfo=pytz.UTC),
        result="Spayed, recovery successful.",
    ),
    VeterinarianRequest(
        id=1_003_007,
        animal_id=1_002_007,
        caregiver_id=1_001_003,
        veterinarian_id=1_001_007,
        request_date=datetime.date(2023, 4, 15),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 4, 25, 0, 0, tzinfo=pytz.UTC),
        result="Treated for ear infection.",
    ),
    VeterinarianRequest(
        id=1_003_008,
        animal_id=1_002_008,
        caregiver_id=1_001_006,
        veterinarian_id=1_001_011,
        request_date=datetime.date(2023, 3, 10),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 3, 20, 0, 0, tzinfo=pytz.UTC),
        result="General health check-up, all good.",
    ),
)