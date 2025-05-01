from fastapi import APIRouter
from sqlmodel import select

from app.core.auth.signup import register_shopper
from app.core.db.conn import DbSession
from app.core.db.user import ShopperCreate, ShopperPublic

from . import service

router = APIRouter(prefix="/shoppers", tags=["shoppers"])


@router.get("/", response_model=list[ShopperPublic])
def get_shoppers(db: DbSession):
    """Retrieves all shoppers from the db"""
    shoppers = service.get_shoppers(db)
    return shoppers


@router.get("/{shopper_id}", response_model=ShopperPublic)
def get_shopper_id(db: DbSession, shopper_id: str):
    """Retrieves a shopper by their id"""
    shopper = service.get_shopper_id(db, shopper_id)
    return shopper


@router.post("/")
def add_shopper(db: DbSession, data: ShopperCreate):
    """Adds a Shopper user"""
    return register_shopper(db, data)
