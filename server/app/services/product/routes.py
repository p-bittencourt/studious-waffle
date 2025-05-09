# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
Product routes module defining API endpoints for product operations.

This module defines all FastAPI routes for product-related operations,
including product creation, retrieval, updating, and deletion.
Routes are divided into public endpoints and vendor-exclusive endpoints
requiring vendor authentication.
"""

from fastapi import APIRouter, Depends, status

from app.core.auth.current_user import VendorUser
from app.core.db.conn import DbSession
from app.services.product.model import ProductPublic, ProductCreate, ProductUpdate

# These exceptions are referenced in docstrings
from app.core.utils.exceptions import (
    BadRequest,
    NotFound,
    CredentialsException,
)

from .service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: DbSession):
    """Get an instance of the ProductService.

    Args:
        db (DbSession): Database session dependency

    Returns:
        ProductService: Service instance for product operations
    """
    return ProductService(db)


@router.get("/", response_model=list[ProductPublic])
def get_products(service: ProductService = Depends(get_product_service)):
    """Retrieve a list of all products.

    Args:
        service (ProductService): Product service dependency

    Returns:
        list[ProductPublic]: List of all product profiles
    """
    products = service.get_products()
    return products


@router.get("/{product_id}", response_model=ProductPublic)
def get_product_id(
    product_id: str, service: ProductService = Depends(get_product_service)
):
    """Retrieve a specific product by its ID.

    Args:
        product_id (str): Unique identifier of the product to retrieve
        service (ProductService): Product service dependency

    Returns:
        ProductPublic: The requested product

    Raises:
        NotFound: If product with given ID doesn't exist (404)
    """
    product = service.get_product_id(product_id)
    return product


## VENDOR EXCLUSIVE ROUTES


@router.post("/", response_model=ProductPublic)
def register_product(
    vendor_user: VendorUser,
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    """Register a new product in the system.

    Requires authentication as a vendor user.

    Args:
        vendor_user (VendorUser): Current authenticated vendor
        product_data (ProductCreate): Product creation data
        service (ProductService): Product service dependency

    Returns:
        ProductPublic: The newly created product

    Raises:
        BadRequest: If product data is invalid
        CredentialsException: If authentication fails (401)
    """
    return service.register_product(vendor_id=vendor_user.id, product_data=product_data)


@router.patch("/{product_id}", response_model=ProductPublic)
def update_product(
    vendor_user: VendorUser,
    product_id: str,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    """Update a product's information.

    Requires authentication as a vendor user.

    Args:
        vendor_user (VendorUser): Current authenticated vendor
        product_id (str): Unique identifier of the product to update
        product_data (ProductUpdate): New data for the product
        service (ProductService): Product service dependency

    Returns:
        ProductPublic: The updated product

    Raises:
        NotFound: If product with given ID doesn't exist (404)
        BadRequest: If no valid update data is provided (400)
        CredentialsException: If authentication fails (401)
    """
    return service.update_product(product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    vendor_user: VendorUser,
    product_id: str,
    service: ProductService = Depends(get_product_service),
):
    """Delete a product from the system.

    Requires authentication as a vendor user.

    Args:
        vendor_user (VendorUser): Current authenticated vendor
        product_id (str): Unique identifier of the product to delete
        service (ProductService): Product service dependency

    Returns:
        None

    Raises:
        NotFound: If product with given ID doesn't exist (404)
        CredentialsException: If authentication fails (401)
    """
    return service.delete_product(product_id)
