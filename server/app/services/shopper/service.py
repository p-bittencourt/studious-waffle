from sqlmodel import Session

from . import repository


def get_shoppers(db: Session):
    """Retrieves all shoppers from the db"""
    shoppers = repository.get_shoppers(db)
    return shoppers


def get_shopper_id(db: Session, shopper_id: str):
    """Retrieves a shopper by ID"""
    shopper = repository.get_shopper_id(db, shopper_id)
    return shopper


def get_shopper_email(db: Session, shopper_email: str):
    """Retrieves a shopper by email"""
    shopper = repository.get_shopper_email(db, shopper_email)
    return shopper
