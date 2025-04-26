"""Database seeding utilities"""

import logging
from enum import Enum
from typing import List, Dict, Any, Callable

import bcrypt
from sqlmodel import Session, select

from .conn import engine
from .user import Vendor, Shopper, UserStatus

logger = logging.getLogger(__name__)


class SeedProfile(str, Enum):
    """Available seeding profiles"""

    MINIMAL = "minimal"
    TESTING = "testing"
    FULL_DEMO = "full_demo"


def create_password_hash(pswd: str) -> str:
    """Create a password hash from plaintext password"""
    pass_bytes = pswd.encode("utf-8")
    return bcrypt.hashpw(pass_bytes, bcrypt.gensalt()).decode("utf-8")


def get_minimal_vendors() -> List[Vendor]:
    """Return a minimal list of demo vendors"""
    return [
        Vendor(
            name="Tech Galaxy",
            phone_number="+1-555-123-4567",
            email="contact@techgalaxy.com",
            status=UserStatus.ACTIVE,
            rating=4.7,
            bank_info={"bank": "Chase", "account": "XXXX1234"},
            comission=10.0,
            specialty="Electronics",
            password_hash=create_password_hash("techpass123"),
            locations=[
                {
                    "type": "store",
                    "street": "Main Street",
                    "number": "123",
                    "zip_code": "10001",
                    "city": "New York",
                    "state": "NY",
                    "country": "USA",
                }
            ],
        ),
        Vendor(
            name="Fashion Avanue",
            phone_number="+1-555-987-6543",
            email="support@fashionavenue.com",
            status=UserStatus.ACTIVE,
            rating=4.5,
            bank_info={"bank": "Bank of America", "account": "XXXX5678"},
            comission=15.0,
            specialty="Clothing",
            password_hash=create_password_hash("fashion456"),
            locations=[
                {
                    "type": "warehouse",
                    "street": "Commerce Blvd",
                    "number": "789",
                    "zip_code": "90210",
                    "city": "Los Angeles",
                    "state": "CA",
                    "country": "USA",
                }
            ],
        ),
    ]


def get_minimal_shoppers() -> List[Shopper]:
    """Returns a minimal list of demo shoppers"""
    return [
        Shopper(
            name="John Doe",
            phone_number="+1-555-111-2222",
            email="john_doe@example.com",
            status=UserStatus.ACTIVE,
            password_hash=create_password_hash("johndoe123"),
            preferences={"theme": "dark", "notifications": True},
            payment_methods=[
                {"type": "credit_card", "last_four": "1234", "provider": "Visa"}
            ],
            wishlist=[1, 3, 5],
            search_history=["laptop", "smartphone", "headphones"],
            order_history=[10001, 10002],
            locations=[
                {
                    "type": "home",
                    "street": "Maple Avenue",
                    "number": "456",
                    "zip_code": "60007",
                    "city": "Chicago",
                    "state": "IL",
                    "country": "USA",
                }
            ],
        ),
        Shopper(
            name="Jane Smith",
            phone_number="+1-555-333-4444",
            email="jane_smith@example.com",
            status=UserStatus.ACTIVE,
            password_hash=create_password_hash("janesmith456"),
            preferences={"theme": "light", "notifications": False},
            payment_methods=[{"type": "paypal", "email": "jane.smith@example.com"}],
            wishlist=[2, 4],
            search_history=["dress", "shoes", "handbag"],
            order_history=[10003],
            locations=[
                {
                    "type": "work",
                    "street": "Tech Park",
                    "number": "789",
                    "complement": "Suite 200",
                    "zip_code": "94043",
                    "city": "Mountain View",
                    "state": "CA",
                    "country": "USA",
                }
            ],
        ),
    ]


# Registry of seed data generators by profile
SEED_REGISTRY: Dict[SeedProfile, Dict[Any, Callable]] = {
    SeedProfile.MINIMAL: {
        Vendor: get_minimal_vendors,
        Shopper: get_minimal_shoppers,
    },
    SeedProfile.TESTING: {
        # To be added
    },
    SeedProfile.FULL_DEMO: {
        # To be added
    },
}


def table_is_empty(session: Session, model) -> bool:
    """Check if a table is empty"""
    return session.exec(select(model)).first() is None


def seed_database(profile: SeedProfile = SeedProfile.MINIMAL):
    """
    Seed the database with initial data if empty

    Args:
        profile: The seeding profile to use. Controls the amount and type of data.
    """

    if profile not in SEED_REGISTRY:
        logger.warning("Seed profile '%s' not found, using MINIMAL instead", profile)
        profile = SeedProfile.MINIMAL

    seed_generators = SEED_REGISTRY[profile]
    if not seed_generators:
        logger.warning("No seed generators found for profile '%s'", profile)

    with Session(engine) as session:
        for model, generator_function in seed_generators.items():
            model_name = model.__name__

            # Check if table is empty and seed if needed
            if table_is_empty(session, model):
                logger.info("Seeding %s table...", model_name)
                items = generator_function()
                for item in items:
                    session.add(item)
                session.commit()
                logger.info("Added %d %s items", len(items), model_name)
            else:
                logger.info(
                    "%s table already contains data, skipping seeding", model_name
                )

    logger.info("Database seeding complete")
