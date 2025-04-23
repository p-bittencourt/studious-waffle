"""Define the user SQLModel"""

from typing import List, Optional
from enum import StrEnum
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Column, JSON

### AUXILIARY STRUCTURES ###


class UserStatus(StrEnum):
    """User enum for configuring status"""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class LocationBase(SQLModel):
    """Location auxiliary data structure"""

    type: str  # pylint: disable=line-too-long # the type could be something like point of sale, warehouse for the vendor | house or office for the shopper, for instance
    street: str
    number: str
    complement: Optional[str] = None
    zip_code: str
    city: str
    state: str
    country: str


# For database storage as JSON
class Location(LocationBase):
    """For db storage as JSON"""

    pass  # pylint: disable=unnecessary-pass


### USER MODELS (not a table) ###


# Base User model
class UserBase(SQLModel):
    """Common User data"""

    name: str
    phone_number: str
    email: EmailStr
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None


### VENDOR MODLES ###


class Vendor(UserBase, table=True):
    """Vendor table - linked to User table"""

    id: Optional[int] = Field(default=None, primary_key=True)
    rating: Optional[float] = None
    bank_info: dict = Field(default={}, sa_column=Column(JSON))
    comission: float = 0.0
    specialty: str = ""
    locations: List[Location] = Field(default=[], sa_column=Column(JSON))


class VendorCreate(UserBase):
    """DTO for creating a vendor"""

    password: str
    rating: Optional[float] = None
    bank_info: Optional[dict] = None
    comission: Optional[float] = 0.0
    specialty: Optional[str] = ""
    locations: Optional[List[LocationBase]] = None


class VendorPublic(UserBase):
    """DTO for returning Vendor data to frontend"""

    id: int
    rating: Optional[float]
    specialty: str
    locations: List[Location] = []


### SHOPPER MODELS ###


class Shopper(UserBase, table=True):
    """Shopper table"""

    id: Optional[int] = Field(default=None, primary_key=True)
    preferences: dict = Field(default={}, sa_column=Column(JSON))
    payment_methods: List[dict] = Field(default=[], sa_column=Column(JSON))
    wishlist: List[int] = Field(
        default=[], sa_column=Column(JSON)
    )  # list of product IDs
    search_history: List[str] = Field(default=[], sa_column=Column(JSON))
    order_history: List[int] = Field(default=[], sa_column=Column(JSON))
    locations: List[Location] = Field(default=[], sa_column=Column(JSON))


class ShopperCreate(UserBase):
    """DTO for creating a shopper"""

    password: str


class ShopperPublic(UserBase):
    """DTO for returning Shopper data to frontend"""

    id: int
    wishlist: Optional[List[int]] = []
    search_history: Optional[List[str]] = []
    order_history: Optional[List[int]] = []
