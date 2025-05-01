from sqlmodel import Session, select

from app.core.db.user import Shopper


def get_shoppers(db: Session):
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
