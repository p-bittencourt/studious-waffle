"""Sign up functions for Shopper and Vendor users"""

import logging

import bcrypt

from sqlmodel import Session
from app.core.db.user import Shopper, ShopperCreate, Vendor, VendorCreate
from app.core.utils.exceptions import BadRequest

logger = logging.getLogger(__name__)


def register_shopper(db: Session, data: ShopperCreate):
    """Adds a new Shopper user"""
    hashed_pswd = hash_password(data.password)
    try:
        new_shopper = Shopper(**data.model_dump(), password_hash=hashed_pswd)
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
    """Registers a new Vendor user"""
    hashed_pswd = hash_password(data.password)
    try:
        new_vendor = Vendor(**data.model_dump(), password_hash=hashed_pswd)
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
    """Gets bytes from the string, returns hash with bcrypt"""
    pass_bytes = pswd.encode("utf-8")
    return bcrypt.hashpw(pass_bytes, bcrypt.gensalt())
