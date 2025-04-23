""""""

import logging

import bcrypt

from sqlmodel import Session
from app.core.db.user import Shopper, ShopperCreate, VendorCreate

logger = logging.getLogger(__name__)


def register_shopper(db: Session, data: ShopperCreate):
    pass_bytes = data.password.encode("utf-8")
    hashed_pswd = bcrypt.hashpw(pass_bytes, bcrypt.gensalt())
    logger.debug("Hashed password: %s", hashed_pswd)
    try:
        new_shopper = Shopper(**data.model_dump())
        logger.debug(f"New shopper: {new_shopper.log_format()}")
    except Exception as e:
        logger.error("Failed to create user")


def register_vendor(data: VendorCreate):
    pass
