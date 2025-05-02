from fastapi import APIRouter

from app.core.auth.signup import register_shopper
from app.core.db.conn import DbSession
from app.core.db.user import ShopperCreate, ShopperPublic, ShopperUpdate

from .service import ShopperService

router = APIRouter(prefix="/shoppers", tags=["shoppers"])


@router.get("/", response_model=list[ShopperPublic])
def get_shoppers(db: DbSession):
    """Retrieves all shoppers from the db"""
    shoppers = ShopperService.get_shoppers(db)
    return shoppers


@router.get("/{shopper_id}", response_model=ShopperPublic)
def get_shopper_id(db: DbSession, shopper_id: str):
    """Retrieves a shopper by their id"""
    shopper = ShopperService.get_shopper_id(db, shopper_id)
    return shopper


@router.post("/{shopper_id}", response_model=ShopperPublic)
def update_shopper(db: DbSession, shopper_id: str, update_data: ShopperUpdate):
    """Updates shopper data"""
    shopper = ShopperService.update_shopper(db, shopper_id, update_data)
    return shopper


@router.delete("/{shopper_id}")
def delete_shopper(db: DbSession, shopper_id: str):
    """Deletes shopper data"""
    return ShopperService.delete_shopper(db, shopper_id)


@router.post("/signup")
def add_shopper(db: DbSession, data: ShopperCreate):
    """Adds a Shopper user"""
    return register_shopper(db, data)
