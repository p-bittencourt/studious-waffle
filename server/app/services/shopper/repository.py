import logging
from typing import List
from sqlmodel import Session, select, update

from app.core.db.user import Shopper, ShopperUpdate
from app.core.utils.exceptions import BadRequest, NotFound

logger = logging.getLogger(__name__)


class ShopperRepository:
    """Repository for Shopper database operations"""

    @classmethod
    def get_shoppers(cls, db: Session) -> List[Shopper]:
        """Retrieves all shoppers from the db"""
        return db.scalars(select(Shopper)).all()

    @classmethod
    def get_shopper_id(cls, db: Session, shopper_id: str) -> Shopper:
        """Retrieves a shopper by ID"""
        return db.scalar(select(Shopper).where(Shopper.id == shopper_id))

    @classmethod
    def get_shopper_email(cls, db: Session, shopper_email: str) -> Shopper:
        """Retrieves a shopper by email"""
        return db.scalar(select(Shopper).where(Shopper.email == shopper_email))

    @classmethod
    def get_shopper_name(cls, db: Session, shopper_name: str) -> Shopper:
        """Retrieves a shopper by name"""
        return db.scalar(select(Shopper).where(Shopper.email == shopper_name))

    @classmethod
    def update_shopper(
        cls, db: Session, shopper_id: str, data: ShopperUpdate
    ) -> Shopper:
        """Updates user data"""
        shopper = cls.get_shopper_id(db, shopper_id)
        if not shopper:
            logger.warning("User with id %s was not found")
            raise NotFound(detail="User not found")

        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_data:
            logger.warning("Couldn't update user %s", shopper.name)
            raise BadRequest(detail="No update data provided")

        stmt = update(Shopper).where(Shopper.id == shopper_id).values(update_data)
        db.exec(stmt)
        db.commit()
        db.refresh(shopper)

        return shopper
