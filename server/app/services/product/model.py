"""
Product model module defining the data models for product operations.

This module defines SQLModel classes for product entities, including database
models, input validation schemas, and response models. It also contains enums
for product categories and statuses.
"""

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.core.db.user import Vendor


class ProductCategory(StrEnum):
    """Product categories enum.

    Defines the available product categories in the system.
    Used for categorizing and filtering products.
    """

    ELECTRONICS = "ELECTRONICS"
    CLOTHING = "CLOTHING"
    HOME_GOODS = "HOME_GOODS"
    BEAUTY = "BEAUTY"
    FOOD = "FOOD"
    OTHER = "OTHER"


class ProductStatus(StrEnum):
    """Product status enum.

    Defines the possible statuses of a product in the system.
    Used for inventory management and availability filtering.
    """

    ACTIVE = "ACTIVE"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    DISCONTINUED = "DISCONTINUED"
    PENDING_REVIEW = "PENDING_REVIEW"


class ProductCreate(SQLModel):
    """Product input data schema.

    Used for validating data when creating a new product.
    Contains the required fields and their validation rules.
    """

    name: str
    price: float
    description: str
    category: ProductCategory = ProductCategory.OTHER
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    sku: Optional[str] = Field(
        default=None, index=True
    )  # Optional but indexed for fast lookups


class Product(ProductCreate, table=True):
    """Product database model.

    Defines the structure of the product table in the database.
    Inherits from ProductCreate and adds system-managed fields.
    """

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
    """Product response model.

    Defines the structure of product data returned to API clients.
    Contains all fields that are safe to expose publicly.
    """

    id: Optional[int]
    vendor_id: Optional[int]
    name: str
    price: float
    description: str
    category: ProductCategory = ProductCategory.OTHER
    tags: Optional[List[str]] = None
    sku: Optional[str] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    status: ProductStatus = ProductStatus.ACTIVE
    created_at: datetime
    updated_at: Optional[datetime] = None
    views_count: int = 0
    sales_count: int = 0
    discount_percentage: float = 0


class ProductUpdate(SQLModel):
    """Product update schema.

    Used for validating data when updating an existing product.
    All fields are optional to support partial updates.
    """

    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[ProductCategory] = None
    tags: Optional[List[str]] = None
    sku: Optional[str] = None
    rating: Optional[float] = None
    stock: Optional[int] = None
    status: Optional[ProductStatus] = None
    updated_at: Optional[datetime] = None
    views_count: Optional[int] = None
    sales_count: Optional[int] = None
    discount_percentage: Optional[float] = None
