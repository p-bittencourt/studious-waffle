"""
Shopper repository module for shopper-specific database operations.

This module implements the repository pattern for Shopper entities,
extending the base repository functionality with any shopper-specific
data access methods.
"""

import logging
from app.core.repository import BaseRepository

logger = logging.getLogger(__name__)


class ShopperRepository(BaseRepository):
    """Repository for Shopper database operations.

    This repository extends BaseRepository to provide specialized data access
    operations for Shopper entities. It inherits all standard CRUD operations
    while allowing for shopper-specific query and business logic extensions.

    Inherits:
        BaseRepository: Provides base CRUD operations for database entities
    """
