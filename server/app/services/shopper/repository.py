import logging
from typing import List
from sqlmodel import Session, select, update

from app.core.db.user import Shopper, ShopperUpdate
from app.core.repository import BaseRepository
from app.core.utils.exceptions import BadRequest

logger = logging.getLogger(__name__)


class ShopperRepository(BaseRepository):
    """Repository for Shopper database operations"""

    def get_shoppers(db: Session) -> List[Shopper]:
        """Retrieves all shoppers from the db"""
        return db.scalars(select(Shopper)).all()

    def get_shopper_id(db: Session, shopper_id: str) -> Shopper:
        """Retrieves a shopper by ID"""
        return db.scalar(select(Shopper).where(Shopper.id == shopper_id))

    def get_shopper_email(db: Session, shopper_email: str) -> Shopper:
        """Retrieves a shopper by email"""
        return db.scalar(select(Shopper).where(Shopper.email == shopper_email))

    def get_shopper_name(db: Session, shopper_name: str) -> Shopper:
        """Retrieves a shopper by name"""
        return db.scalar(select(Shopper).where(Shopper.email == shopper_name))

    def update_shopper(db: Session, shopper: Shopper, data: ShopperUpdate) -> Shopper:
        """Updates shopper data"""
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_data:
            logger.warning("Couldn't update shopper %s", shopper.name)
            raise BadRequest(detail="No update data provided")

        stmt = update(Shopper).where(Shopper.id == shopper.id).values(update_data)
        db.exec(stmt)
        db.commit()
        db.refresh(shopper)

        return shopper

    def delete_shopper(db: Session, shopper: Shopper):
        """Deletes shopper data"""
        shopper_id = shopper.id
        db.delete(shopper)
        db.commit()
        logger.info("Deleted shopper #%s", shopper_id)
