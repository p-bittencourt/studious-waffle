"""
Shopper service module for business logic related to shoppers.

This module implements the service layer for Shopper entities, handling
business logic, validation, and orchestrating repository operations. It
acts as an intermediary between the API endpoints and the repository layer.
"""

from datetime import datetime
import logging
from typing import List
from sqlmodel import Session

from app.core.db.user import Shopper, ShopperPublic, ShopperUpdate
from app.core.models.common import OrderItemCreate
from app.core.utils.exceptions import NotFound
from app.services.product.service import ProductService
from .repository import ShopperRepository

logger = logging.getLogger(__name__)


class ShopperService:
    """Service for managing shopper-related business operations.

    This service encapsulates the business logic for shopper entities,
    including retrieval, creation, updates, and deletion operations.
    It uses ShopperRepository for data access and applies necessary
    business rules and validations.
    """

    def __init__(self, db: Session):
        """Initialize the service with a database session.

        Args:
            db (Session): SQLModel database session
        """
        self.db = db
        self.repository = ShopperRepository(db)
        self.product_service = ProductService(db)

    def get_shoppers(self) -> List[ShopperPublic]:
        """Retrieve all shoppers from the database.

        Returns:
            List[ShopperPublic]: A list of all shopper instances
        """
        return self.repository.get_items(Shopper)

    def get_shopper_id(self, shopper_id: str) -> ShopperPublic:
        """Retrieve a shopper by their ID.

        Args:
            shopper_id (str): The unique identifier of the shopper

        Returns:
            ShopperPublic: The shopper instance

        Raises:
            NotFound: If no shopper with the given ID exists
        """
        shopper = self.repository.get_item_id(Shopper, shopper_id)
        if not shopper:
            logger.warning("User with id %s was not found", shopper_id)
            raise NotFound(detail="User not found")

        return shopper

    def get_shopper_email(self, shopper_email: str) -> ShopperPublic:
        """Retrieve a shopper by their email address.

        Args:
            shopper_email (str): The email address of the shopper

        Returns:
            ShopperPublic: The shopper instance

        Raises:
            NotFound: If no shopper with the given email exists
        """
        shopper = self.repository.get_item_by_property(Shopper, "email", shopper_email)
        if not shopper:
            logger.warning("User with email %s was not found", shopper_email)
            raise NotFound(detail="User not found")

        return shopper

    def update_shopper(
        self, shopper_id: str, update_data: ShopperUpdate
    ) -> ShopperPublic:
        """Update a shopper's information.

        Args:
            shopper_id (str): The unique identifier of the shopper to update
            update_data (ShopperUpdate): The data to update the shopper with

        Returns:
            ShopperPublic: The updated shopper instance

        Raises:
            NotFound: If no shopper with the given ID exists
            BadRequest: If no valid update data is provided
        """
        shopper = self.get_shopper_id(shopper_id)

        updated_shopper = self.repository.update_item(Shopper, shopper, update_data)
        return updated_shopper

    def delete_shopper(self, shopper_id: str) -> None:
        """Delete a shopper from the system.

        Args:
            shopper_id (str): The unique identifier of the shopper to delete

        Returns:
            None

        Raises:
            NotFound: If no shopper with the given ID exists
        """
        shopper = self.get_shopper_id(shopper_id)
        return self.repository.delete_item(shopper)

    ### SHOPPING CART METHODS
    def add_to_cart(self, shopper_id: str, item_data: OrderItemCreate) -> ShopperPublic:
        """Add an item to the shopper's shopping cart.

        Args:
            shopper_id (str): The unique identifier of the shopper
            item_data (OrderItemCreate): The item to add to the cart

        Returns:
            ShopperPublic: The updated shopper instance

        Raises:
            NotFound: If no shopper with the given ID exists
        """
        shopper = self.get_shopper_id(shopper_id)

        # Validate that the user has a shopping cart
        if not shopper.shopping_cart:
            shopper.shopping_cart = {"items": [], "updated_at": None}

        # Validate the product_id exists
        _ = self.product_service.get_product_id(item_data.product_id)

        # Add or update the item in the cart
        found = False
        for i, item in enumerate(shopper.shopping_cart["items"]):
            if item["product_id"] == item_data.product_id:
                shopper.shopping_cart["items"][i]["quantity"] += item_data.quantity
                found = True
                break

        if not found:
            # Add new item as a dictionary
            shopper.shopping_cart["items"].append(
                {"product_id": item_data.product_id, "quantity": item_data.quantity}
            )

        # Update timestamp
        shopper.shopping_cart["updated_at"] = datetime.utcnow().isoformat()

        # Create update data with just the shopping cart
        update_data = ShopperUpdate(shopping_cart=shopper.shopping_cart)

        # Use the specialized repository method
        return self.update_shopper(shopper_id, update_data)

    def remove_from_cart(
        self, shopper_id: str, product_id: str, quantity: int = 1
    ) -> ShopperPublic:
        """Remove an item from the shopper's shopping cart.

        Args:
            shopper_id (str): The unique identifier of the shopper
            product_id (int): The ID of the product to remove

        Returns:
            ShopperPublic: The updated shopper instance

        Raises:
            NotFound: If no shopper with the given ID exists or product not in cart
        """
        shopper = self.get_shopper_id(shopper_id)

        # if the user doesn't have a shopping cart, create an empty one and return
        if not shopper.shopping_cart:
            shopper.shopping_cart = {"items": [], "updated_at": None}
            update_data = ShopperUpdate(shopping_cart=shopper.shopping_cart)
            return self.update_shopper(shopper_id, update_data)

        # Find the item and remove or reduce quantity
        found = False
        for i, item in enumerate(shopper.shopping_cart["items"]):
            if item["product_id"] == int(product_id):
                found = True
                if quantity is None or quantity >= item["quantity"]:
                    # Remove the entire item
                    shopper.shopping_cart["items"].pop(i)
                else:
                    # Reduce quantity
                    shopper.shopping_cart["items"][i]["quantity"] -= quantity
                break

            if not found:
                logger.warning(
                    "Product %s not found in shopper %s's cart", product_id, shopper_id
                )

        shopper.shopping_cart["updated_at"] = datetime.utcnow().isoformat()
        update_data = ShopperUpdate(shopping_cart=shopper.shopping_cart)

        return self.update_shopper(shopper_id, update_data)

    def clear_shopping_cart(self, shopper_id: str) -> ShopperPublic:
        """Clear all items from the shopper's shopping cart.

        Args:
            shopper_id (str): The unique identifier of the shopper

        Returns:
            ShopperPublic: The updated shopper instance

        Raises:
            NotFound: If no shopper with the given ID exists
        """
        shopper = self.get_shopper_id(shopper_id)
        shopper.shopping_cart = {
            "items": [],
            "updated_at": datetime.utcnow().isoformat(),
        }
        update_data = ShopperUpdate(shopping_cart=shopper.shopping_cart)

        return self.update_shopper(shopper_id, update_data)
