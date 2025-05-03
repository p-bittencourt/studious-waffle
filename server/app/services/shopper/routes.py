"""
Shopper routes module defining API endpoints for shopper operations.

This module defines all FastAPI routes for shopper-related operations,
including user registration, profile management, and administrative functions.
Routes are divided into protected (requiring authentication) and unprotected sections.
"""

from fastapi import APIRouter, Depends, status

from app.core.auth.current_user import ShopperUser
from app.core.auth.signup import register_shopper
from app.core.db.conn import DbSession
from app.core.db.user import ShopperCreate, ShopperPublic, ShopperUpdate
from app.core.utils.exceptions import (
    BadRequest,
    NotFound,
    CredentialsException,
)  # pylint: disable=unused-import

from .service import ShopperService

router = APIRouter(prefix="/shoppers", tags=["shoppers"])


def get_shopper_service(db: DbSession):
    """Get an instance of the ShopperService.

    Args:
        db (DbSession): Database session dependency

    Returns:
        ShopperService: Service instance for shopper operations
    """
    return ShopperService(db)


### UNPROTECTED ROUTES ###
@router.post(
    "/signup", response_model=ShopperPublic, status_code=status.HTTP_201_CREATED
)
def add_shopper(db: DbSession, data: ShopperCreate):
    """Register a new shopper in the system.

    Args:
        db (DbSession): Database session dependency
        data (ShopperCreate): Shopper registration data including email and password

    Returns:
        ShopperPublic: The newly created shopper profile

    Raises:
        BadRequest: If registration data is invalid or email already exists
    """
    return register_shopper(db, data)


### PROTECTED ROUTES ###
@router.get("/", response_model=list[ShopperPublic])
def get_shoppers(
    current_user: ShopperUser, service: ShopperService = Depends(get_shopper_service)
):
    """Retrieve a list of all shoppers.

    Requires authentication as a shopper user.

    Args:
        current_user (ShopperUser): Current authenticated shopper
        service (ShopperService): Shopper service dependency

    Returns:
        list[ShopperPublic]: List of all shopper profiles
    """
    shoppers = service.get_shoppers()
    return shoppers


@router.get("/{shopper_id}", response_model=ShopperPublic)
def get_shopper_id(
    current_user: ShopperUser,
    shopper_id: str,
    service: ShopperService = Depends(get_shopper_service),
):
    """Retrieve a specific shopper by their ID.

    Requires authentication as a shopper user.

    Args:
        current_user (ShopperUser): Current authenticated shopper
        shopper_id (str): Unique identifier of the shopper to retrieve
        service (ShopperService): Shopper service dependency

    Returns:
        ShopperPublic: The requested shopper profile

    Raises:
        NotFound: If shopper with given ID doesn't exist (404)
        CredentialsException: If authentication fails (401)
    """
    shopper = service.get_shopper_id(shopper_id)
    return shopper


@router.post("/{shopper_id}", response_model=ShopperPublic)
def update_shopper(
    current_user: ShopperUser,
    shopper_id: str,
    update_data: ShopperUpdate,
    service: ShopperService = Depends(get_shopper_service),
):
    """Update a shopper's profile information.

    Requires authentication as a shopper user.

    Args:
        current_user (ShopperUser): Current authenticated shopper
        shopper_id (str): Unique identifier of the shopper to update
        update_data (ShopperUpdate): New data for the shopper profile
        service (ShopperService): Shopper service dependency

    Returns:
        ShopperPublic: The updated shopper profile

    Raises:
        NotFound: If shopper with given ID doesn't exist (404)
        BadRequest: If no valid update data is provided (400)
        CredentialsException: If authentication fails (401)
    """
    shopper = service.update_shopper(shopper_id, update_data)
    return shopper


@router.delete("/{shopper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shopper(
    current_user: ShopperUser,
    shopper_id: str,
    service: ShopperService = Depends(get_shopper_service),
):
    """Delete a shopper from the system.

    Requires authentication as a shopper user.

    Args:
        current_user (ShopperUser): Current authenticated shopper
        shopper_id (str): Unique identifier of the shopper to delete
        service (ShopperService): Shopper service dependency

    Returns:
        None

    Raises:
        NotFound: If shopper with given ID doesn't exist (404)
        CredentialsException: If authentication fails (401)
    """
    return service.delete_shopper(shopper_id)
