"""Factory for producing test users"""

from datetime import datetime
import factory
from app.core.db.user import Shopper, UserStatus, Vendor


class ShopperFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Shopper factory"""

    class Meta:
        """Factory meta data"""

        model = Shopper  # SQLAlchemy model
        sqlalchemy_session_persistence = (
            "commit"  # Commit the session after creating the user instance
        )

    # Faker properties
    name = factory.Faker("name")
    phone_number = factory.Faker("phone_number")
    email = factory.Faker("email")
    password_hash = factory.Faker("sha256")
    status = UserStatus.ACTIVE
    created_at = factory.LazyFunction(datetime.utcnow)
    last_login = None
    preferences = {}
    payment_methods = []
    wishlist = []
    search_history = []
    order_history = []
    locations = []


class VendorFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Vendor factory"""

    class Meta:
        """Factory meta data"""

        model = Vendor  # SQLAlchemy model
        sqlalchemy_session_persistence = "commit"

    # Faker properties
    name = factory.Faker("company")
    phone_number = factory.Faker("phone_number")
    email = factory.Faker("company_email")
    password_hash = factory.Faker("sha256")
    status = UserStatus.ACTIVE
    created_at = factory.LazyFunction(datetime.utcnow)
    last_login = None
    rating = factory.Faker("pyfloat", min_value=1.0, max_value=5.0)
    bank_info = {}
    comission = factory.Faker("pyfloat", min_value=0.0, max_value=0.3)
    specialty = factory.Faker("bs")
    locations = []
