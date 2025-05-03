"""
Vendor repository module for vendor-specific database operations.

This module implements the repository pattern for Vendor entities,
extending the base repository functionality with any vendor-specific
data access methods.
"""

import logging
from app.core.repository import BaseRepository

logger = logging.getLogger(__name__)


class VendorRepository(BaseRepository):
    """Repository for Vendor database operations.

    This repository extends BaseRepository to provide specialized data access
    operations for Vendor entities. It inherits all standard CRUD operations
    while allowing for vendor-specific query and business logic extensions.

    Inherits:
        BaseRepository: Provides base CRUD operations for database entities
    """
