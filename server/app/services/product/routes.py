from fastapi import APIRouter, Depends, status

from app.core.auth.current_user import VendorUser
from app.core.db.conn import DbSession
from app.services.product.model import ProductPublic, ProductCreate, ProductUpdate

from .service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(db: DbSession):
    return ProductService(db)


@router.get("/", response_model=list[ProductPublic])
def get_products(service: ProductService = Depends(get_product_service)):
    products = service.get_products()
    return products


@router.get("/{product_id}", response_model=ProductPublic)
def get_product_id(
    product_id: str, service: ProductService = Depends(get_product_service)
):
    product = service.get_product_id(product_id)
    return product


## VENDOR EXCLUSIVE ROUTES


@router.post("/", response_model=ProductPublic)
def register_product(
    vendor_user: VendorUser,
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return service.register_product(vendor_id=vendor_user.id, product_data=product_data)


@router.patch("/{product_id}", response_model=ProductPublic)
def update_product(
    vendor_user: VendorUser,
    product_id: str,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    return service.update_product(product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    vendor_user: VendorUser,
    product_id: str,
    service: ProductService = Depends(get_product_service),
):
    return service.delete_product(product_id)
