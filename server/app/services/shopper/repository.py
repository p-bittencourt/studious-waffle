import logging
from sqlmodel import Session, select, update

from app.core.db.user import Shopper, ShopperUpdate
from app.core.utils.exceptions import BadRequest, NotFound


logger = logging.getLogger(__name__)


def get_shoppers(db: Session) -> Shopper:
    """Retrieves all shoppers from the db"""
    return db.scalars(select(Shopper)).all()


def get_shopper_id(db: Session, shopper_id: str):
    """Retrieves a shopper by ID"""
    return db.scalar(select(Shopper).where(Shopper.id == shopper_id))


def get_shopper_email(db: Session, shopper_email: str):
    """Retrieves a shopper by email"""
    return db.scalar(select(Shopper).where(Shopper.email == shopper_email))


def get_shopper_name(db: Session, shopper_name: str):
    """Retrieves a shopper by name"""
    return db.scalar(select(Shopper).where(Shopper.email == shopper_name))


def update_shopper(db: Session, shopper_id: str, data: ShopperUpdate) -> Shopper:
    """Updates user data"""
    shopper = get_shopper_id(db, shopper_id)
    if not shopper:
        raise NotFound()

    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        logger.warning("Couldn't update user %s", shopper.name)
        raise BadRequest(detail="No update data provided")

    stmt = update(Shopper).where(Shopper.id == shopper_id).values(update_data)
    db.exec(stmt)
    db.commit()

    db.refresh(shopper)

    return shopper
