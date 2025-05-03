from fastapi import APIRouter, Depends

from app.core.auth.current_user import ShopperUser
from app.core.auth.signup import register_shopper
from app.core.db.conn import DbSession
from app.core.db.user import ShopperCreate, ShopperPublic, ShopperUpdate

from .service import ShopperService

router = APIRouter(prefix="/shoppers", tags=["shoppers"])


def get_shopper_service(db: DbSession):
    return ShopperService(db)


### UNPROTECTED ROUTES ###
@router.post("/signup")
def add_shopper(db: DbSession, data: ShopperCreate):
    """Adds a Shopper user"""
    return register_shopper(db, data)


### PROTECTED ROUTES ###
@router.get("/", response_model=list[ShopperPublic])
def get_shoppers(
    current_user: ShopperUser, service: ShopperService = Depends(get_shopper_service)
):
    """Retrieves all shoppers from the db"""
    shoppers = service.get_shoppers()
    return shoppers


@router.get("/{shopper_id}", response_model=ShopperPublic)
def get_shopper_id(
    current_user: ShopperUser,
    shopper_id: str,
    service: ShopperService = Depends(get_shopper_service),
):
    """Retrieves a shopper by their id"""
    shopper = service.get_shopper_id(shopper_id)
    return shopper


@router.post("/{shopper_id}", response_model=ShopperPublic)
def update_shopper(
    current_user: ShopperUser,
    shopper_id: str,
    update_data: ShopperUpdate,
    service: ShopperService = Depends(get_shopper_service),
):
    """Updates shopper data"""
    shopper = service.update_shopper(shopper_id, update_data)
    return shopper


@router.delete("/{shopper_id}")
def delete_shopper(
    current_user: ShopperUser,
    shopper_id: str,
    service: ShopperService = Depends(get_shopper_service),
):
    """Deletes shopper data"""
    return service.delete_shopper(shopper_id)
