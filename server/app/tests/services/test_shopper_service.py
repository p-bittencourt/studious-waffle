"""Test module for the ShopperService class."""

import pytest
from sqlmodel import Session

from app.core.db.user import ShopperUpdate
from app.core.utils.exceptions import NotFound
from app.services.shopper.service import ShopperService
from app.tests.factories.users import ShopperFactory


class TestShopperService:
    """Test cases for ShopperService functionality"""

    def test_get_shoppers(self, db: Session):
        """Tests retrieving all shoppers"""
        # Arrange
        service = ShopperService(db)
        # Create multiple shoppers
        shopper1 = ShopperFactory()
        shopper2 = ShopperFactory()
        shopper3 = ShopperFactory()

        # Act
        shoppers = service.get_shoppers()

        # Assert
        assert len(shoppers) >= 3
