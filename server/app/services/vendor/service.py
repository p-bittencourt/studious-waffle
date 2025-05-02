import logging
from typing import List
from sqlmodel import Session

from app.core.db.user import Vendor, VendorPublic, VendorUpdate
from app.core.utils.exceptions import NotFound
from .repository import VendorRepository

logger = logging.getLogger(__name__)


class VendorService:

    def get_vendors(db: Session) -> List[VendorPublic]:
        """Retrieves all vendors from the db"""
        return VendorRepository.get_items(db, Vendor)

    def get_vendor_id(db: Session, vendor_id: str) -> VendorPublic:
        """Retrieves a vendor by ID"""
        vendor = VendorRepository.get_item_id(db, Vendor, vendor_id)
        if not vendor:
            logger.warning("User with id %s was not found")
            raise NotFound(detail="User not found")

        return vendor

    def get_vendor_email(db: Session, vendor_email: str) -> VendorPublic:
        """Retrieves a vendor by email"""
        vendor = VendorRepository.get_item_by_property(
            db, Vendor, "email", vendor_email
        )
        if not vendor:
            logger.warning("User with id %s was not found")
            raise NotFound(detail="User not found")

        return vendor

    def update_vendor(
        db: Session, vendor_id: str, update_data: VendorUpdate
    ) -> VendorPublic:
        """Updates vendor data"""
        vendor = VendorService.get_vendor_id(db, vendor_id)

        updated_vendor = VendorRepository.update_item(db, Vendor, vendor, update_data)
        return updated_vendor

    def delete_vendor(db: Session, vendor_id: str):
        """Deletes a vendor"""
        vendor = VendorService.get_vendor_id(db, vendor_id)
        return VendorRepository.delete_item(db, vendor)
