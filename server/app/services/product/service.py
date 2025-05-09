import logging
from typing import List
from sqlmodel import Session

from app.core.utils.exceptions import NotFound
from app.services.product.model import Product, ProductPublic
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
