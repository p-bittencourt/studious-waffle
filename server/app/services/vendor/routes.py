from fastapi import APIRouter
from sqlmodel import select

from app.core.auth.signup import register_vendor
from app.core.db.conn import DbSession
from app.core.db.user import Vendor, VendorCreate, VendorPublic


router = APIRouter(prefix="/vendors", tags=["vendors"])


@router.get("/", response_model=list[VendorPublic])
def get_vendors(db: DbSession):
    """Retrieves all vendors from the db"""
    vendors = db.scalars(select(Vendor)).all()
    return vendors


@router.post("/")
def add_vendor(db: DbSession, data: VendorCreate):
    """Adds a vendor user"""
    return register_vendor(db, data)
