from ..models import User


#                 User, password
USER_SEEDS: list[tuple[User, str]] = [
    (
        User(
            id=1_001_001,
            username="michael",
            first_name="Michael",
            last_name="Wee",
            email="wee@gmail.com",
            contact_info="0907000001",
            role=User.Role.ADMINISTRATOR,
        ),
        "password",
    ),
    (
        User(
            id=1_001_002,
            username="tampol",
            first_name="Tamara",
            last_name="Pollar",
            email="dui.fusce@aol.ca",
            contact_info="1-634-667-2515",
            role=User.Role.CAREGIVER,
        ),
        "password",
    ),
    (
        User(
            id=1_001_003,
            username="harvey",
            first_name="Upton",
            last_name="Harvey",
            email="sed.molestie@google.net",
            contact_info="214-7437",
            role=User.Role.CAREGIVER,
        ),
        "password",
    ),
    (
        User(
            id=1_001_004,
            username="blakeRae",
            first_name="Rae",
            last_name="Blake",
            email="sed@outlook.edu",
            contact_info="321-3272",
            role=User.Role.VETERINARIAN,
        ),
        "password",
    ),
]
