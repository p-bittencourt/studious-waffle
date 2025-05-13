"""
Order service module for business logic related to orders.

This module implements the service layer for Order entities, handling
business logic, validation, and orchestrating repository operations. It
acts as an intermediary between the API endpoints and the repository layer.
"""

import logging
from typing import List
from sqlmodel import Session

from app.core.utils.exceptions import BadRequest, NotFound
from app.services.order.model import (
    Order,
    OrderCreate,
    OrderItem,
    OrderItemCreate,
    OrderPublic,
    OrderUpdate,
)
from app.services.order.repository import OrderRepository
from app.services.product.service import ProductService


logger = logging.getLogger(__name__)


class OrderService:
    """Service for managing order-related business operations.

    This service encapsulates the business logic for order entities,
    including retrieval, creation, updates, and deletion operations.
    It uses ProductRepository for data access and applies necessary
    business rules and validations.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = OrderRepository(db)
        self.product_service = ProductService(db)

    def get_orders(self) -> List[OrderPublic]:
        return self.repository.get_items(Order)

    def get_order_id(self, order_id: str) -> OrderPublic:
        order = self.repository.get_item_id(Order, order_id)
        if not order:
            logger.warning("Order with id %s was not found", order_id)
            raise NotFound(detail="Order not found")

        return order

    def register_order(self, shopper_id: str, order_data: OrderCreate) -> OrderPublic:
        # Validate that all products exist
        order_items = order_data.ordered_items
        valid_items = self.validate_items_exist(order_items)
        if not valid_items:
            raise BadRequest(detail=f"Provide a valid product_id to confirm an order.")

        order = Order(**order_data.model_dump(), shopper_id=shopper_id)
        result = self.repository.add_item(Order, order)
        order_id = result.id

        self.register_order_items(order_items, order_id)

        return result

    def validate_items_exist(self, order_items: List[OrderItemCreate]) -> bool:
        for order_item in order_items:
            try:
                _ = self.product_service.get_product_id(order_item.product_id)
            except NotFound:
                return False
        return True

    def register_order_items(
        self, order_items: List[OrderItemCreate], order_id: str
    ) -> None:
        for order_item in order_items:
            item_object = OrderItem(**order_item.model_dump(), order_id=order_id)
            self.repository.add_item(OrderItem, item_object)

    def update_order(self, order_id: str, update_data: OrderUpdate) -> OrderPublic:
        order = self.get_order_id(order_id)
        # TODO: update update_time property

        updated_order = self.repository.update_item(Order, order, update_data)
        return updated_order

    def delete_order(self, order_id: str) -> None:
        order = self.get_order_id(order_id)
        return self.repository.delete_item(order)
