"""
Shopper service module for business logic related to shoppers.

This module implements the service layer for Shopper entities, handling
business logic, validation, and orchestrating repository operations. It
acts as an intermediary between the API endpoints and the repository layer.
"""

import logging
from typing import List
from sqlmodel import Session

from app.core.db.user import Shopper, ShopperPublic, ShopperUpdate
from app.core.utils.exceptions import NotFound
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
