from fastapi import APIRouter

from app.core.auth.signup import register_vendor
from app.core.db.conn import DbSession
from app.core.db.user import VendorCreate, VendorPublic, VendorUpdate

from .service import VendorService


router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("/", response_model=list[VendorPublic])
def get_vendors(db: DbSession):
    """Retrieves all vendors from the db"""
    vendors = VendorService.get_vendors(db)
    return vendors


@router.post("/signup")
def add_vendor(db: DbSession, data: VendorCreate):
    """Adds a vendor user"""
    return register_vendor(db, data)


@router.get("/{vendor_id}", response_model=VendorPublic)
def get_vendor_id(db: DbSession, vendor_id: str):
    """Retrieves a vendor by their id"""
    vendor = VendorService.get_vendor_id(db, vendor_id)
    return vendor


@router.post("/{vendor_id}", response_model=VendorPublic)
def update_vendor(db: DbSession, vendor_id: str, update_data: VendorUpdate):
    """Updates vendor data"""
    vendor = VendorService.update_vendor(db, vendor_id, update_data)
    return vendor


@router.delete("/{vendor_id}")
def delete_vendor(db: DbSession, vendor_id: str):
    """Deletes vendor data"""
    return VendorService.delete_vendor(db, vendor_id)
