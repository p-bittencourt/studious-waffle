from fastapi import APIRouter, Depends

from app.core.auth.current_user import VendorUser
from app.core.auth.signup import register_vendor
from app.core.db.conn import DbSession
from app.core.db.user import VendorCreate, VendorPublic, VendorUpdate

from .service import VendorService


router = APIRouter(prefix="/vendors", tags=["vendors"])


def get_vendor_dependency(db: DbSession):
    return VendorService(db)


### UNPROTECTED ROUTES ###
@router.post("/signup")
def add_vendor(db: DbSession, data: VendorCreate):
    """Adds a vendor user"""
    return register_vendor(db, data)


### PROTECTED ROUTES ###
@router.get("/", response_model=list[VendorPublic])
def get_vendors(
    current_user: VendorUser, service: VendorService = Depends(get_vendor_dependency)
):
    """Retrieves all vendors from the db"""
    vendors = service.get_vendors()
    return vendors


@router.get("/{vendor_id}", response_model=VendorPublic)
def get_vendor_id(
    current_user: VendorUser,
    vendor_id: str,
    service: VendorService = Depends(get_vendor_dependency),
):
    """Retrieves a vendor by their id"""
    vendor = service.get_vendor_id(vendor_id)
    return vendor


@router.post("/{vendor_id}", response_model=VendorPublic)
def update_vendor(
    current_user: VendorUser,
    vendor_id: str,
    update_data: VendorUpdate,
    service: VendorService = Depends(get_vendor_dependency),
):
    """Updates vendor data"""
    vendor = service.update_vendor(vendor_id, update_data)
    return vendor


@router.delete("/{vendor_id}")
def delete_vendor(
    current_user: VendorUser,
    vendor_id: str,
    service: VendorService = Depends(get_vendor_dependency),
):
    """Deletes vendor data"""
    return service.delete_vendor(vendor_id)
