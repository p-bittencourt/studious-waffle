from typing import List
from sqlmodel import Session

from app.core.db.user import ShopperPublic, ShopperUpdate

from .repository import ShopperRepository


class ShopperService:

    def get_shoppers(db: Session) -> List[ShopperPublic]:
        """Retrieves all shoppers from the db"""
        shoppers = ShopperRepository.get_shoppers(db)
        return shoppers

    def get_shopper_id(db: Session, shopper_id: str) -> ShopperPublic:
        """Retrieves a shopper by ID"""
        shopper = ShopperRepository.get_shopper_id(db, shopper_id)
        return shopper

    def get_shopper_email(db: Session, shopper_email: str) -> ShopperPublic:
        """Retrieves a shopper by email"""
        shopper = ShopperRepository.get_shopper_email(db, shopper_email)
        return shopper

    def update_shopper(
        db: Session, shopper_id: str, update_data: ShopperUpdate
    ) -> ShopperPublic:
        """Updates shopper data"""
        shopper = ShopperRepository.update_shopper(db, shopper_id, update_data)
        return shopper
