import logging
from app.core.repository import BaseRepository

logger = logging.getLogger(__name__)


class VendorRepository(BaseRepository):
    """Repository for Vendor database operations"""
