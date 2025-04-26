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

    pass


### USER MODELS (not a table) ###


# Base User model


# Base with only common fields that users will provide on creation
class UserCreateBase(SQLModel):
    """Common User Input data"""

    name: str
    phone_number: str
    email: EmailStr


# System-managed fields
class UserSystemFields(SQLModel):
    """Common User data"""

    password_hash: str = ""
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None


class UserBase(UserCreateBase, UserSystemFields):
    """Complete user data for DB"""

    pass


### VENDOR MODELS ###


class Vendor(UserBase, table=True):
    """Vendor table - linked to User table"""

    id: Optional[int] = Field(default=None, primary_key=True)
    rating: Optional[float] = None
    bank_info: dict = Field(default={}, sa_column=Column(JSON))
    comission: float = 0.0
    specialty: str = ""
    locations: List[Location] = Field(default=[], sa_column=Column(JSON))

    def log_format(self) -> str:
        """Format for logging purposes"""
        return (
            f"VENDOR [id={self.id}] | {self.name} | {self.email} | "
            f"Status: {self.status} | Created: {self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else 'N/A'}"
        )


class VendorCreate(UserBase):
    """DTO for creating a vendor"""

    password: str


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

    def log_format(self) -> str:
        """Format for logging purposes"""
        return (
            f"SHOPPER [id={self.id}] | {self.name} | {self.email} | "
            f"Status: {self.status} | Created: {self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else 'N/A'}"
        )


class ShopperCreate(UserCreateBase):
    """DTO for creating a shopper"""

    password: str


class ShopperPublic(SQLModel):
    """DTO for returning Shopper data to frontend"""

    id: int
    name: str
    phone_number: str
    email: EmailStr
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    preferences: dict = Field(default={}, sa_column=Column(JSON))
    payment_methods: List[dict] = Field(default=[], sa_column=Column(JSON))
    wishlist: List[int] = Field(
        default=[], sa_column=Column(JSON)
    )  # list of product IDs
    search_history: List[str] = Field(default=[], sa_column=Column(JSON))
    order_history: List[int] = Field(default=[], sa_column=Column(JSON))
    locations: List[Location] = Field(default=[], sa_column=Column(JSON))
