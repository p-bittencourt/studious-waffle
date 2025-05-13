"""Define the user SQLModel"""

from typing import TYPE_CHECKING, List, Optional
from enum import StrEnum
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, Column, JSON

from app.core.models.common import Location
from app.services.order.model import OrderItemCreate

if TYPE_CHECKING:
    from app.services.product.model import Product
    from app.services.order.model import Order

### AUXILIARY STRUCTURES ###


class UserStatus(StrEnum):
    """User enum for configuring status"""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class ShoppingCartBase(SQLModel):
    """Shopper user's shopping cart"""

    items: List[OrderItemCreate]
    updated_at: Optional[datetime]


class ShoppingCart(ShoppingCartBase):
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

    # Relationships
    products: List["Product"] = Relationship(back_populates="vendor")

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
    created_at: datetime = None
    last_login: Optional[datetime] = None
    rating: Optional[float] = None
    bank_info: dict = None
    comission: float = 0.0
    specialty: str = ""
    locations: List[Location] = None


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
    shopping_cart: ShoppingCart = Field(
        default_factory=lambda: ShoppingCart(items=[], updated_at=None),
        sa_column=Column(JSON),
    )

    # Relationship
    orders: List["Order"] = Relationship(back_populates="shopper")

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
    created_at: datetime = None
    last_login: Optional[datetime] = None
    preferences: dict = None
    payment_methods: List[dict] = None
    wishlist: List[int] = None
    search_history: List[str] = None
    order_history: List[int] = None
    locations: List[Location] = None
    shopping_cart: Optional[ShoppingCart] = None


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
    shopping_cart: Optional[ShoppingCart] = None
