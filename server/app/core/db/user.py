"""Define the user SQLModel"""

from sqlmodel import Date, Field, SQLModel
from enum import StrEnum


class UserStatus(StrEnum):
    """User enum for configuring status"""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Location:
    """Location auxiliary data structure"""

    type: str  # this could be something like point of sale, warehouse for the vendor | house or office for the shopper, for instance
    street: str
    number: str
    complement: str
    zip_code: str
    city: str
    state: str
    country: str


class User(SQLModel):
    """Common User data (not a table)"""

    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone_number: str
    email: str
    created_at: Date
    last_login: Date
    status: UserStatus


class Vendor(User, table=True):
    """Vendor table"""

    rating: str
    bank_info: str
    comission: str
    locations: list[Location]
    specialty: str


class Shopper(User, table=True):
    """Shopper table"""

    preferences: str
    payment_methods: str
    wishlist: str
    search_history: str
    order_history: str
    locations: list[Location]
