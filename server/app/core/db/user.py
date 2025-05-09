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

    type: str  # the type could be something like point of sale, warehouse for the vendor | house or office for the shopper, for instance
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
    """Common User data added by the system"""

    password_hash: str = ""
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None


# Data input by user to login
class UserLoginFields(SQLModel):
    """User email and password"""

    email: EmailStr
    password: str


class UserBase(UserCreateBase, UserSystemFields):
    """Complete user data for DB"""

    pass


### VENDOR MODELS ###


class Vendor(UserBase, table=True):
    """Vendor table"""

    id: Optional[int] = Field(default=None, primary_key=True)
    rating: Optional[float] = None
    bank_info: dict = Field(default={}, sa_column=Column(JSON))
    comission: float = 0.0
    specialty: str = ""
    locations: List[Location] = Field(default=[], sa_column=Column(JSON))

    def log_format(self) -> str:
        """Format for logging purposes"""
        created_time = (
            self.created_at.strftime("%Y-%m-%d %H:%M")
            if hasattr(self.created_at, "strftime")
            else "N/A"
        )  # Formats created_at datetime if present
        return (
            f"VENDOR [id={self.id}] | {self.name} | {self.email} | "
            f"Status: {self.status} | Created: {created_time}"
        )


class VendorCreate(UserCreateBase):
    """DTO for creating a vendor"""

    password: str


class VendorPublic(SQLModel):
    """DTO for returning Vendor data to frontend"""

    id: int
    name: str
    phone_number: str
    email: EmailStr
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    rating: Optional[float] = None
    bank_info: dict = Field(default={}, sa_column=Column(JSON))
    comission: float = 0.0
    specialty: str = ""
    locations: List[Location] = Field(default=[], sa_column=Column(JSON))


class VendorUpdate(SQLModel):
    """DTO for data update"""

    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[UserStatus] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    rating: Optional[float] = None
    bank_info: Optional[dict] = None
    comission: Optional[float] = None
    specialty: Optional[str] = None
    locations: Optional[List[Location]] = None


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
        created_time = (
            self.created_at.strftime("%Y-%m-%d %H:%M")
            if hasattr(self.created_at, "strftime")
            else "N/A"
        )  # Formats created_at datetime if present
        return (
            f"SHOPPER [id={self.id}] | {self.name} | {self.email} | "
            f"Status: {self.status} | Created: {created_time}"
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


class ShopperUpdate(SQLModel):
    """DTO for data update"""

    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[UserStatus] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    preferences: Optional[dict] = None
    payment_methods: Optional[List[dict]] = None
    wishlist: Optional[List[int]] = None  # list of product IDs
    search_history: Optional[List[str]] = None
    order_history: Optional[List[int]] = None
    locations: Optional[List[Location]] = None
