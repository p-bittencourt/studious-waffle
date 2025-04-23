""""""

import logging
from sqlmodel import Session
from app.core.db.user import Shopper, ShopperCreate, VendorCreate

logger = logging.getLogger(__name__)


def register_shopper(db: Session, data: ShopperCreate):
    hashed_pswd = salt_password(data.password)
    logger.debug("Hashed password: %s", hashed_pswd)
    try:
        new_shopper = Shopper(**data.model_dump())
        logger.debug(f"New shopper: {new_shopper.log_format()}")
    except Exception as e:
        logger.error("Failed to create user")


def register_vendor(data: VendorCreate):
    hashed_pswd = salt_password(data.password)


def salt_password(pswd: str) -> str:
    salt = "12e29184y"
    return pswd + salt
