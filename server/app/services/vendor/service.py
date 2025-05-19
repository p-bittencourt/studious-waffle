"""
Vendor service module for business logic related to vendors.

This module implements the service layer for Vendor entities, handling
business logic, validation, and orchestrating repository operations. It
acts as an intermediary between the API endpoints and the repository layer.
"""

import logging
from typing import List
from sqlmodel import Session

from app.core.db.user import Vendor, VendorPublic, VendorUpdate
from app.core.utils.exceptions import NotFound
from .repository import VendorRepository

logger = logging.getLogger(__name__)


class VendorService:
    """Service for managing vendor-related business operations.

    This service encapsulates the business logic for vendor entities,
    including retrieval, creation, updates, and deletion operations.
    It uses VendorRepository for data access and applies necessary
    business rules and validations.
    """

    def __init__(self, db: Session):
        """Initialize the service with a database session.

        Args:
            db (Session): SQLModel database session
        """
        self.db = db
        self.repository = VendorRepository(db)

    def get_vendors(self) -> List[VendorPublic]:
        """Retrieve all vendors from the database.

        Returns:
            List[VendorPublic]: A list of all vendor instances
        """
        return self.repository.get_items(Vendor)

    def get_vendor_id(self, vendor_id: str) -> VendorPublic:
        """Retrieve a vendor by their ID.

        Args:
            vendor_id (str): The unique identifier of the vendor

        Returns:
            VendorPublic: The vendor instance

        Raises:
            NotFound: If no vendor with the given ID exists
        """
        vendor = self.repository.get_item_id(Vendor, vendor_id)
        if not vendor:
            logger.warning("User with id %s was not found", vendor_id)
            raise NotFound(detail="User not found")

        return vendor

    def get_vendor_email(self, vendor_email: str) -> VendorPublic:
        """Retrieve a vendor by their email address.

        Args:
            vendor_email (str): The email address of the vendor

        Returns:
            VendorPublic: The vendor instance

        Raises:
            NotFound: If no vendor with the given email exists
        """
        vendor = self.repository.get_item_by_property(Vendor, "email", vendor_email)
        if not vendor:
            logger.warning("User with email %s was not found", vendor_email)
            raise NotFound(detail="User not found")

        return vendor

    def update_vendor(self, vendor_id: str, update_data: VendorUpdate) -> VendorPublic:
        """Update a vendor's information.

        Args:
            vendor_id (str): The unique identifier of the vendor to update
            update_data (VendorUpdate): The data to update the vendor with

        Returns:
            VendorPublic: The updated vendor instance

        Raises:
            NotFound: If no vendor with the given ID exists
            BadRequest: If no valid update data is provided
        """
        vendor = self.get_vendor_id(vendor_id)

        updated_vendor = self.repository.update_item(Vendor, vendor, update_data)
        return updated_vendor

    def delete_vendor(self, vendor_id: str) -> None:
        """Delete a vendor from the system.

        Args:
            vendor_id (str): The unique identifier of the vendor to delete

        Returns:
            None

        Raises:
            NotFound: If no vendor with the given ID exists
        """
        vendor = self.get_vendor_id(vendor_id)
        return self.repository.delete_item(vendor)
