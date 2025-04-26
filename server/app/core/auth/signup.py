""""""

import logging

import bcrypt

from sqlmodel import Session
from app.core.db.user import Shopper, ShopperCreate, Vendor, VendorCreate
from app.core.utils.exceptions import BadRequest

logger = logging.getLogger(__name__)


def register_shopper(db: Session, data: ShopperCreate):
    hashed_pswd = hash_password(data.password)
    try:
        new_shopper = Shopper(**data.model_dump(), password_hash=hashed_pswd)
        logger.debug(f"New shopper: {new_shopper}")
        db.add(new_shopper)
        db.commit()
        db.refresh(new_shopper)
        logger.info(
            "Created Shopper %s with email %s", new_shopper.name, new_shopper.email
        )
        return {"status": "success", "message": "User registered successfully"}
    except Exception as e:
        logger.error("Failed to create user")
        raise BadRequest() from e


def register_vendor(db: Session, data: VendorCreate):
    hashed_pswd = hash_password(data.password)
    logger.debug("Hashed password: %s", hashed_pswd)
    try:
        new_vendor = Vendor(**data.model_dump())
        db.add(new_vendor)
        db.commit()
        db.refresh(new_vendor)
        logger.info(
            "Created Vendor %s with email %s", new_vendor.name, new_vendor.email
        )
        return {"status": "success", "message": "User registered successfully"}
    except Exception as e:
        logger.error("Failed to create user")
        raise BadRequest() from e


def hash_password(pswd: str):
    pass_bytes = pswd.encode("utf-8")
    return bcrypt.hashpw(pass_bytes, bcrypt.gensalt())
