from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.core.db.user import Vendor


class ProductCategory(StrEnum):
    """Product categories enum"""

    ELECTRONICS = "ELECTRONICS"
    CLOTHING = "CLOTHING"
    HOME_GOODS = "HOME_GOODS"
    BEAUTY = "BEAUTY"
    FOOD = "FOOD"
    OTHER = "OTHER"


class ProductStatus(StrEnum):
    """Product status enum"""

    ACTIVE = "ACTIVE"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    DISCONTINUED = "DISCONTINUED"
    PENDING_REVIEW = "PENDING_REVIEW"


class ProductCreate(SQLModel):
    """Product Input data"""

    name: str
    price: float
    description: str
    category: ProductCategory = ProductCategory.OTHER
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    sku: Optional[str] = Field(
        default=None, index=True
    )  # Optional but indexed for fast lookups


class Product(ProductCreate, table=True):
    """Product table"""

    id: Optional[int] = Field(default=None, primary_key=True)
    vendor_id: Optional[int] = Field(default=None, foreign_key="vendor.id")
    rating: Optional[float] = None
    stock: Optional[int] = None
    status: ProductStatus = ProductStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    views_count: int = 0
    sales_count: int = 0
    discount_percentage: float = 0

    # Relationships
    vendor: Optional["Vendor"] = Relationship(back_populates="products")


class ProductPublic(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    vendor_id: Optional[int] = Field(default=None, foreign_key="vendor.id")
    name: str
    price: float
    description: str
    category: ProductCategory = ProductCategory.OTHER
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    sku: Optional[str] = Field(
        default=None, index=True
    )  # Optional but indexed for fast lookups
    rating: Optional[float] = None
    stock: Optional[int] = None
    status: ProductStatus = ProductStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    views_count: int = 0
    sales_count: int = 0
    discount_percentage: float = 0


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[ProductCategory] = None
    tags: Optional[List[str]] = None
    sku: Optional[str] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    status: Optional[ProductStatus] = None
    views_count: Optional[int] = None
    sales_count: Optional[int] = None
    discount_percentage: Optional[float] = None
