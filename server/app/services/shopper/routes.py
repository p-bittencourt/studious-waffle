from fastapi import APIRouter
from sqlmodel import select

from app.core.auth.signup import register_shopper
from app.core.db.conn import DbSession
from app.core.db.user import Shopper, ShopperCreate, ShopperPublic


router = APIRouter(prefix="/shoppers", tags=["shoppers"])


@router.get("/", response_model=list[ShopperPublic])
def get_shoppers(db: DbSession):
    """Retrieves all shoppers from the db"""
    shoppers = db.scalars(select(Shopper)).all()
    return shoppers


@router.post("/")
def add_shopper(db: DbSession, data: ShopperCreate):
    """Adds a Shopper user"""
    return register_shopper(db, data)
