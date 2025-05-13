"""
Order repository module for order-specific database operations.

This module implements the repository pattern for Order entities,
extending the base repository functionality with any order-specific
data access methods.
"""

import logging
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from app.core.repository import BaseRepository
from app.services.order.model import Order, OrderItem, OrderItemCreate

logger = logging.getLogger(__name__)


class OrderRepository(BaseRepository):
    """Repository for Order database operations.

    This repository extends BaseRepository to provide specialized data access
    operations for Order entities. It inherits all standard CRUD operations
    while allowing for shopper-specific query and business logic extensions.

    Inherits:
        BaseRepository: Provides base CRUD operations for database entities
    """

    def create_order_with_items(
        self, order: Order, order_items: List[OrderItemCreate]
    ) -> Optional[Order]:
        """Create an order and its items in a single transaction.

        Args:
            order: The order object to create
            order_items: List of order items to associate with the order

        Returns:
            The created order with its ID assigned, or None if operation fails

        Raises:
            SQLAlchemyError: If a specific database operation fails
        """
        try:
            self.db.add(order)
            self.db.flush()

            for item_data in order_items:
                item = OrderItem(
                    order_id=order.id,
                    product_id=item_data.product_id,
                    quantity=item_data.quantity,
                    unit_price=item_data.unit_price,
                    total_price=item_data.total_price,
                )
                self.db.add(item)

            self.db.commit()
            self.db.refresh(order)
            logger.info("Created order #%s with %d items", order.id, len(order_items))

            return order
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error("Failed to create order with items: %s", str(e))
            raise e
