import logging
from typing import List
from sqlmodel import Session

from app.core.db.user import Shopper, ShopperPublic, ShopperUpdate
from app.core.utils.exceptions import NotFound
from .repository import ShopperRepository

logger = logging.getLogger(__name__)


class ShopperService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ShopperRepository(db)

    def get_shoppers(self) -> List[ShopperPublic]:
        """Retrieves all shoppers from the db"""
        return self.repository.get_items(Shopper)

    def get_shopper_id(self, shopper_id: str) -> ShopperPublic:
        """Retrieves a shopper by ID"""
        shopper = self.repository.get_item_id(Shopper, shopper_id)
        if not shopper:
            logger.warning("User with id %s was not found", shopper_id)
            raise NotFound(detail="User not found")

        return shopper

    def get_shopper_email(self, shopper_email: str) -> ShopperPublic:
        """Retrieves a shopper by email"""
        shopper = self.repository.get_item_by_property(Shopper, "email", shopper_email)
        if not shopper:
            logger.warning("User with email %s was not found", shopper_email)
            raise NotFound(detail="User not found")

        return shopper

    def update_shopper(
        self, shopper_id: str, update_data: ShopperUpdate
    ) -> ShopperPublic:
        """Updates shopper data"""
        shopper = self.get_shopper_id(shopper_id)

        updated_shopper = self.repository.update_item(Shopper, shopper, update_data)
        return updated_shopper

    def delete_shopper(self, shopper_id: str):
        """Deletes a shopper"""
        shopper = self.get_shopper_id(shopper_id)
        return self.repository.delete_item(shopper)
