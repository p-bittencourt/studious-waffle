"""
Order model module defining the data models for order operations.

This module defines SQLModel classes for order entities, including database
models, input validation schemas, and response models. It also contains enums
for order categories and statuses.
"""

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from app.core.models.common import Location, OrderItem, OrderItemCreate, OrderItemPublic

if TYPE_CHECKING:
    from app.core.db.user import Shopper

### ENUMS


class OrderStatus(StrEnum):
    """Order status enum.

    Defines the possible statuses of an order in the system.
    """

    IN_PROGRESS = "IN_PROGRESS"
    CONCLUDED = "CONCLUDED"
    CANCELLED = "CANCELLED"


class PaymentStatus(StrEnum):
    """Payment statys enum.

    Defines the possible statuses of a payment in the system.
    """

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


### ORDER MODELS ###
### Order base model with information that's common to the table and to the validation schema of OrderCreate


class OrderBase(SQLModel):
    """Order base model"""

    # Payment info
    payment_method: Optional[str] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING

    # Shipping info
    delivery_location: Location = Field(sa_column=Column(JSON))
    shipping_method: Optional[str] = None
    tracking_number: Optional[str] = None
    estimated_delivery: Optional[datetime] = None

    # Discounts and promotions
    discount_code: Optional[str] = None
    discount_amount: float = 0.0

    # Tax and totals
    subtotal: float
    tax_amount: float = 0.0
    shipping_cost: float = 0.0
    total_value: float


### Order create with a separate property that's not stored on the db, it's for validating items added to the order
class OrderCreate(OrderBase):
    """Model to validate incoming items to create the order.

    It's a separate entity from Order table to avoid issues trying to create a column with ordered_items
    """

    # Order items
    ordered_items: List[OrderItemCreate]


### Order table
class Order(OrderBase, table=True):
    """Order database model.

    Defines the structure of the order table in the database.
    Inherits from OrderCreate and adds system-managed fields.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    shopper_id: Optional[int] = Field(default=None, foreign_key="shopper.id")
    status: OrderStatus = OrderStatus.IN_PROGRESS
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    # Relationships
    items: List["OrderItem"] = Relationship(back_populates="order")
    shopper: "Shopper" = Relationship(back_populates="orders")


class OrderPublic(SQLModel):
    """Order response model.

    Defines the structure of order data returned to API clients.
    Contains all fields that are safe to expose publicly.
    """

    id: int
    shopper_id: int
    items: List[OrderItemPublic]
    status: OrderStatus = OrderStatus.IN_PROGRESS

    # Payment info
    payment_method: Optional[str] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING

    # Shipping info
    delivery_location: Location
    shipping_method: Optional[str] = None
    tracking_number: Optional[str] = None
    estimated_delivery: Optional[datetime] = None

    # Discounts and promotions
    discount_code: Optional[str] = None
    discount_amount: float = 0.0

    # Tax and totals
    subtotal: float
    tax_amount: float = 0.0
    shipping_cost: float = 0.0
    total_value: float

    created_at: datetime
    updated_at: Optional[datetime] = None


class OrderUpdate(SQLModel):
    """Order update schema.

    Used for balidating data when updating an existing order.
    All fields are optional to support partial updates.
    """

    items: Optional[List[OrderItem]]
    status: Optional[OrderStatus]

    # Payment info
    payment_method: Optional[str]
    payment_status: Optional[PaymentStatus]

    # Shipping info
    delivery_location: Optional[Location]
    shipping_method: Optional[str]
    tracking_number: Optional[str]
    estimated_delivery: Optional[datetime]

    # Discounts and promotions
    discount_code: Optional[str]
    discount_amount: Optional[float]

    # Tax and totals
    subtotal: Optional[float]
    tax_amount: Optional[float]
    shipping_cost: Optional[float]
    total_value: Optional[float]
    updated_at: Optional[datetime]
