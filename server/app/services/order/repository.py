"""
Order repository module for order-specific database operations.

This module implements the repository pattern for Order entities,
extending the base repository functionality with any order-specific
data access methods.
"""

from app.core.repository import BaseRepository


class OrderRepository(BaseRepository):
    """Repository for Order database operations.

    This repository extends BaseRepository to provide specialized data access
    operations for Order entities. It inherits all standard CRUD operations
    while allowing for shopper-specific query and business logic extensions.

    Inherits:
        BaseRepository: Provides base CRUD operations for database entities
    """
