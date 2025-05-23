"""
Product service module for business logic related to products.

This module implements the service layer for Product entities, handling
business logic, validation, and orchestrating repository operations. It
acts as an intermediary between the API endpoints and the repository layer.
"""

import logging
from typing import List
from sqlmodel import Session

from app.core.utils.exceptions import NotFound
from app.services.product.model import (
    Product,
    ProductCreate,
    ProductPublic,
    ProductUpdate,
)
from app.services.product.repository import ProductRepository

logger = logging.getLogger(__name__)


class ProductService:
    """Service for managing product-related business operations.

    This service encapsulates the business logic for product entities,
    including retrieval, creation, updates, and deletion operations.
    It uses ProductRepository for data access and applies necessary
    business rules and validations.
    """

    def __init__(self, db: Session):
        """Initialize the service with a database session.

        Args:
            db (Session): SQLModel database session
        """
        self.db = db
        self.repository = ProductRepository(db)

    def get_products(self) -> List[ProductPublic]:
        """Retrieve all products from the database.

        Returns:
            List[ProductPublic]: A list of all product instances
        """
        return self.repository.get_items(Product)

    def get_product_id(self, product_id: str) -> ProductPublic:
        """Retrieve a product by its ID.

        Args:
            product_id (str): The unique identifier of the product

        Returns:
            ProductPublic: The product instance

        Raises:
            NotFound: If no product with the given ID exists
        """
        product = self.repository.get_item_id(Product, product_id)
        if not product:
            logger.warning("Product with id %s was not found", product_id)
            raise NotFound(detail="Product not found")

        return product

    def register_product(
        self, vendor_id: str, product_data: ProductCreate
    ) -> ProductPublic:
        """Register a new product in the system.

        Args:
            vendor_id (str): The unique identifier of the vendor creating the product
            product_data (ProductCreate): The data for creating the product

        Returns:
            ProductPublic: The newly created product instance

        Raises:
            BadRequest: If product data is invalid or missing required fields
        """
        product = Product(**product_data.model_dump(), vendor_id=vendor_id)
        result = self.repository.add_item(Product, product)
        return result

    def update_product(
        self, product_id: str, update_data: ProductUpdate
    ) -> ProductPublic:
        """Update a product's information.

        Args:
            product_id (str): The unique identifier of the product to update
            update_data (ProductUpdate): The data to update the product with

        Returns:
            ProductPublic: The updated product instance

        Raises:
            NotFound: If no product with the given ID exists
            BadRequest: If no valid update data is provided
        """
        product = self.get_product_id(product_id)

        updated_product = self.repository.update_item(Product, product, update_data)
        return updated_product

    def delete_product(self, product_id: str) -> None:
        """Delete a product from the system.

        Args:
            product_id (str): The unique identifier of the product to delete

        Returns:
            None

        Raises:
            NotFound: If no product with the given ID exists
        """
        product = self.get_product_id(product_id)
        return self.repository.delete_item(product)
