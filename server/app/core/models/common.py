"""Common models shared across multiple modules"""

from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel


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


### ORDER ITEMS MODELS
### Order items establish the relationship between an Order and its Products


class OrderItemCreate(SQLModel):
    """Schema for validating order items in API requests"""

    product_id: int
    quantity: int
    unit_price: float = None  # Optional in request, calculated in service
    total_price: float = None  # Optional in request, calculated in service


class OrderItemPublic(SQLModel):
    """Schema for structuring OrderItem data to be returned from the API"""

    product_id: int
    quantity: int
    unit_price: float
    total_price: float

    # Additional info to expose
    product_name: Optional[str] = None


class OrderItem(SQLModel, table=True):
    """Ordered items class.

    Used for organizing product and amount on an order.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    unit_price: float  # price at time of order
    total_price: float

    # Relationships
    order: Optional["Order"] = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship()


# Type hints for the circular references
if TYPE_CHECKING:
    from app.services.order.model import Order
    from app.services.product.model import Product
