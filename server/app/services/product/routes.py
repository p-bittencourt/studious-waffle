from fastapi import APIRouter, Depends, status

from app.core.db.conn import DbSession
from app.services.product.model import ProductPublic

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
