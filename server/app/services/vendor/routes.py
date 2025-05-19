# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
Vendor routes module defining API endpoints for vendor operations.

This module defines all FastAPI routes for vendor-related operations,
including user registration, profile management, and administrative functions.
Routes are divided into protected (requiring authentication) and unprotected sections.
"""

from fastapi import APIRouter, Depends, status

# Imported for dependency injection - used by FastAPI
from app.core.auth.current_user import VendorUser
from app.core.auth.signup import register_vendor
from app.core.db.conn import DbSession
from app.core.db.user import VendorCreate, VendorPublic, VendorUpdate

# These exceptions are referenced in docstrings
from app.core.utils.exceptions import (
    BadRequest,
    NotFound,
    CredentialsException,
)

from .service import VendorService


router = APIRouter(prefix="/vendors", tags=["vendors"])


def get_vendor_dependency(db: DbSession):
    """Get an instance of the VendorService.

    Args:
        db (DbSession): Database session dependency

    Returns:
        VendorService: Service instance for vendor operations
    """
    return VendorService(db)


### UNPROTECTED ROUTES ###
@router.post(
    "/signup", response_model=VendorPublic, status_code=status.HTTP_201_CREATED
)
def add_vendor(db: DbSession, data: VendorCreate):
    """Register a new vendor in the system.

    Args:
        db (DbSession): Database session dependency
        data (VendorCreate): Vendor registration data including email and password

    Returns:
        VendorPublic: The newly created vendor profile

    Raises:
        BadRequest: If registration data is invalid or email already exists
    """
    return register_vendor(db, data)


### PROTECTED ROUTES ###
@router.get("/", response_model=list[VendorPublic])
def get_vendors(
    current_user: VendorUser, service: VendorService = Depends(get_vendor_dependency)
):
    """Retrieve a list of all vendors.

    Requires authentication as a vendor user.

    Args:
        current_user (VendorUser): Current authenticated vendor
        service (VendorService): Vendor service dependency

    Returns:
        list[VendorPublic]: List of all vendor profiles
    """
    vendors = service.get_vendors()
    return vendors


@router.get("/{vendor_id}", response_model=VendorPublic)
def get_vendor_id(
    current_user: VendorUser,
    vendor_id: str,
    service: VendorService = Depends(get_vendor_dependency),
):
    """Retrieve a specific vendor by their ID.

    Requires authentication as a vendor user.

    Args:
        current_user (VendorUser): Current authenticated vendor
        vendor_id (str): Unique identifier of the vendor to retrieve
        service (VendorService): Vendor service dependency

    Returns:
        VendorPublic: The requested vendor profile

    Raises:
        NotFound: If vendor with given ID doesn't exist (404)
        CredentialsException: If authentication fails (401)
    """
    vendor = service.get_vendor_id(vendor_id)
    return vendor


@router.patch("/{vendor_id}", response_model=VendorPublic)
def update_vendor(
    current_user: VendorUser,
    vendor_id: str,
    update_data: VendorUpdate,
    service: VendorService = Depends(get_vendor_dependency),
):
    """Update a vendor's profile information.

    Requires authentication as a vendor user.

    Args:
        current_user (VendorUser): Current authenticated vendor
        vendor_id (str): Unique identifier of the vendor to update
        update_data (VendorUpdate): New data for the vendor profile
        service (VendorService): Vendor service dependency

    Returns:
        VendorPublic: The updated vendor profile

    Raises:
        NotFound: If vendor with given ID doesn't exist (404)
        BadRequest: If no valid update data is provided (400)
        CredentialsException: If authentication fails (401)
    """
    vendor = service.update_vendor(vendor_id, update_data)
    return vendor


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(
    current_user: VendorUser,
    vendor_id: str,
    service: VendorService = Depends(get_vendor_dependency),
):
    """Delete a vendor from the system.

    Requires authentication as a vendor user.

    Args:
        current_user (VendorUser): Current authenticated vendor
        vendor_id (str): Unique identifier of the vendor to delete
        service (VendorService): Vendor service dependency

    Returns:
        None

    Raises:
        NotFound: If vendor with given ID doesn't exist (404)
        CredentialsException: If authentication fails (401)
    """
    return service.delete_vendor(vendor_id)
