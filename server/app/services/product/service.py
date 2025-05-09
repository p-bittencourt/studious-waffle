import logging
from typing import List
from sqlmodel import Session

from app.core.utils.exceptions import NotFound
from app.services.product.model import (
    Product,
    ProductCreate,
    ProductPublic,
    ProductUpdate,
)
from app.services.product.repository import ProductRepository

logger = logging.getLogger(__name__)


class ProductService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = ProductRepository(db)

    def get_products(self) -> List[ProductPublic]:
        return self.repository.get_items(Product)

    def get_product_id(self, product_id: str) -> ProductPublic:
        product = self.repository.get_item_id(Product, product_id)
        if not product:
            logger.warning("Product with id %s was not found", product_id)
            raise NotFound(detail="Product not found")

        return product

    def register_product(
        self, vendor_id: str, product_data: ProductCreate
    ) -> ProductPublic:
        product = Product(**product_data.model_dump(), vendor_id=vendor_id)
        result = self.repository.add_item(Product, product)
        return result

    def update_product(
        self, product_id: str, update_data: ProductUpdate
    ) -> ProductPublic:
        product = self.get_product_id(product_id)

        updated_product = self.repository.update_item(Product, product, update_data)
        return updated_product

    def delete_product(self, product_id: str) -> None:
        product = self.get_product_id(product_id)
        return self.repository.delete_item(product)
