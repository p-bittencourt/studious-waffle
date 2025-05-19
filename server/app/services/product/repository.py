"""
Product repository module for product-specific database operations.

This module implements the repository pattern for Product entities,
extending the base repository functionality with any product-specific
data access methods.
"""

import logging
from app.core.repository import BaseRepository

logger = logging.getLogger(__name__)


class ProductRepository(BaseRepository):
    """Repository for Product database operations.

    This repository extends BaseRepository to provide specialized data access
    operations for Product entities. It inherits all standard CRUD operations
    while allowing for shopper-specific query and business logic extensions.

    Inherits:
        BaseRepository: Provides base CRUD operations for database entities
    """
