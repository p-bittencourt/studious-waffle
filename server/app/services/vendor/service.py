import logging
from typing import List
from sqlmodel import Session

from app.core.db.user import Vendor, VendorPublic, VendorUpdate
from app.core.utils.exceptions import NotFound
from .repository import VendorRepository

logger = logging.getLogger(__name__)


class VendorService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = VendorRepository(db)

    def get_vendors(self) -> List[VendorPublic]:
        """Retrieves all vendors from the db"""
        return self.repository.get_items(Vendor)

    def get_vendor_id(self, vendor_id: str) -> VendorPublic:
        """Retrieves a vendor by ID"""
        vendor = self.repository.get_item_id(Vendor, vendor_id)
        if not vendor:
            logger.warning("User with id %s was not found")
            raise NotFound(detail="User not found")

        return vendor

    def get_vendor_email(self, vendor_email: str) -> VendorPublic:
        """Retrieves a vendor by email"""
        vendor = self.repository.get_item_by_property(Vendor, "email", vendor_email)
        if not vendor:
            logger.warning("User with id %s was not found")
            raise NotFound(detail="User not found")

        return vendor

    def update_vendor(self, vendor_id: str, update_data: VendorUpdate) -> VendorPublic:
        """Updates vendor data"""
        vendor = self.get_vendor_id(vendor_id)

        updated_vendor = self.repository.update_item(Vendor, vendor, update_data)
        return updated_vendor

    def delete_vendor(self, vendor_id: str):
        """Deletes a vendor"""
        vendor = self.get_vendor_id(vendor_id)
        return self.repository.delete_item(vendor)
