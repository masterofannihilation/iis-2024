from ..models import VeterinarianRequest
import datetime
import pytz

HEALTH_RECORD_SEEDS = (
    VeterinarianRequest(
        id=1_003_000,
        animal_id=1_002_000,
        caregiver_id=1_001_002,
        request_date=datetime.date(2023, 11, 5),
        status=VeterinarianRequest.Status.REQUESTED,
        examination_date=None,
        result=None,
        description="Initial health check.",
    ),
    VeterinarianRequest(
        id=1_003_001,
        animal_id=1_002_001,
        caregiver_id=1_001_003,
        veterinarian_id=1_001_007,
        request_date=datetime.date(2023, 10, 25),
        status=VeterinarianRequest.Status.SCHEDULED,
        examination_date=datetime.datetime(2023, 11, 10, 10, 30, tzinfo=pytz.UTC),
        result=None,
        description="Scheduled vaccination and general check-up.",
    ),
    VeterinarianRequest(
        id=1_003_002,
        animal_id=1_002_001,
        caregiver_id=1_001_006,
        veterinarian_id=1_001_011,
        request_date=datetime.date(2023, 9, 20),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 10, 1, 14, 0, tzinfo=pytz.UTC),
        result="Healthy, no issues found.",
        description="Routine check-up and vaccination.",
    ),
    VeterinarianRequest(
        id=1_003_003,
        animal_id=1_002_003,
        caregiver_id=1_001_010,
        veterinarian_id=1_001_015,
        request_date=datetime.date(2023, 8, 15),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 8, 25, 11, 45, tzinfo=pytz.UTC),
        result="Minor skin infection treated.",
        description="Skin infection treatment after examination.",
    ),
    VeterinarianRequest(
        id=1_003_004,
        animal_id=1_002_004,
        caregiver_id=1_001_014,
        veterinarian_id=1_001_019,
        request_date=datetime.date(2023, 7, 10),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 7, 20, 8, 30, tzinfo=pytz.UTC),
        result="Vaccinated and dewormed.",
        description="Routine vaccinations and deworming.",
    ),
    VeterinarianRequest(
        id=1_003_005,
        animal_id=1_002_005,
        caregiver_id=1_001_018,
        veterinarian_id=1_001_023,
        request_date=datetime.date(2023, 6, 20),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 6, 30, 15, 0, tzinfo=pytz.UTC),
        result="Dental check-up completed.",
        description="Routine dental health check.",
    ),
    VeterinarianRequest(
        id=1_003_006,
        animal_id=1_002_006,
        caregiver_id=1_001_002,
        request_date=datetime.date(2023, 5, 30),
        status=VeterinarianRequest.Status.REQUESTED,
        description="Spay surgery.",
    ),
    VeterinarianRequest(
        id=1_003_007,
        animal_id=1_002_007,
        caregiver_id=1_001_003,
        veterinarian_id=1_001_007,
        request_date=datetime.date(2023, 4, 15),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 4, 25, 16, 0, tzinfo=pytz.UTC),
        result="Treated for ear infection.",
        description="Ear infection treatment.",
    ),
    VeterinarianRequest(
        id=1_003_008,
        animal_id=1_002_008,
        caregiver_id=1_001_006,
        veterinarian_id=1_001_011,
        request_date=datetime.date(2023, 3, 10),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 3, 20, 12, 30, tzinfo=pytz.UTC),
        result="General health check-up, all good.",
        description="Routine health check-up.",
    ),
    VeterinarianRequest(
        id=1_003_010,
        animal_id=1_002_000,
        caregiver_id=1_001_002,
        veterinarian_id=1_001_004,
        request_date=datetime.date(2023, 11, 22),
        status=VeterinarianRequest.Status.SCHEDULED,
        examination_date=datetime.datetime(2023, 12, 5, 9, 30, tzinfo=pytz.UTC),
        result=None,
        description="Scheduled follow-up health check.",
    ),
    VeterinarianRequest(
        id=1_003_011,
        animal_id=1_002_001,
        caregiver_id=1_001_003,
        veterinarian_id=1_001_007,
        request_date=datetime.date(2023, 11, 5),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 11, 10, 10, 0, tzinfo=pytz.UTC),
        result="Vaccinated, no issues found.",
        description="Vaccination and general health check.",
    ),
    VeterinarianRequest(
        id=1_003_012,
        animal_id=1_002_002,
        caregiver_id=1_001_010,
        veterinarian_id=1_001_015,
        request_date=datetime.date(2023, 10, 5),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 10, 10, 13, 30, tzinfo=pytz.UTC),
        result="Minor leg injury, treated successfully.",
        description="Treatment for leg injury.",
    ),
    VeterinarianRequest(
        id=1_003_013,
        animal_id=1_002_003,
        caregiver_id=1_001_014,
        veterinarian_id=1_001_019,
        request_date=datetime.date(2023, 8, 5),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 8, 15, 14, 0, tzinfo=pytz.UTC),
        result="Healthy, no new issues.",
        description="Routine health check.",
    ),
    VeterinarianRequest(
        id=1_003_014,
        animal_id=1_002_004,
        caregiver_id=1_001_014,
        request_date=datetime.date(2023, 7, 5),
        status=VeterinarianRequest.Status.REQUESTED,
        description="Treatment for skin rash.",
    ),
    VeterinarianRequest(
        id=1_003_015,
        animal_id=1_002_005,
        caregiver_id=1_001_018,
        request_date=datetime.date(2023, 6, 25),
        status=VeterinarianRequest.Status.REQUESTED,
        examination_date=None,
        result=None,
        description="Dental check-up.",
    ),
    VeterinarianRequest(
        id=1_003_016,
        animal_id=1_002_006,
        caregiver_id=1_001_002,
        veterinarian_id=1_001_004,
        request_date=datetime.date(2023, 5, 29),
        status=VeterinarianRequest.Status.COMPLETED,
        examination_date=datetime.datetime(2023, 6, 5, 9, 30, tzinfo=pytz.UTC),
        result="No health concerns.",
        description="General health check.",
    ),
    VeterinarianRequest(
        id=1_003_018,
        animal_id=1_002_008,
        caregiver_id=1_001_006,
        veterinarian_id=1_001_011,
        request_date=datetime.date(2023, 3, 20),
        status=VeterinarianRequest.Status.SCHEDULED,
        examination_date=datetime.datetime(2023, 4, 1, 10, 0, tzinfo=pytz.UTC),
        result=None,
        description="Scheduled health check.",
    ),
)
