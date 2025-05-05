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
        # Verify that our created shoppers are in the results
        shopper_ids = [shopper.id for shopper in shoppers]
        assert shopper1.id in shopper_ids
        assert shopper2.id in shopper_ids
        assert shopper3.id in shopper_ids

    def test_get_shopper_id_found(self, db: Session):
        """Tests retrieving a shopper by ID when it exists"""
        # Arrange
        service = ShopperService(db)
        shopper = ShopperFactory()

        # Act
        retrieved_shopper = service.get_shopper_id(shopper.id)

        # Assert
        assert retrieved_shopper.id == shopper.id
        assert retrieved_shopper.email == shopper.email

    def test_get_shopper_id_not_found(self, db: Session):
        """Tests retrieving a shopper by ID when it doesn't exist"""
        # Arrange
        service = ShopperService(db)
        non_existent_id = 2233

        # Act & Assert
        with pytest.raises(NotFound) as exc_info:
            service.get_shopper_id(non_existent_id)
        assert "User not found" in str(exc_info.value.detail)

    def test_get_shopper_email_found(self, db: Session):
        """Tests retrieving a shopper by email when it exists"""
        # Arrange
        service = ShopperService(db)
        shopper = ShopperFactory()

        # Act
        retrieved_shopper = service.get_shopper_email(shopper.email)

        # Assert
        assert retrieved_shopper.id == shopper.id
        assert retrieved_shopper.email == shopper.email

    def test_get_shopper_email_not_found(self, db: Session):
        """Tests retrieving a shopper by email when it doesn't exist"""
        # Arrange
        service = ShopperService(db)
        non_existent_email = "nonexistent@example.com"

        # Act & Assert
        with pytest.raises(NotFound) as exc_info:
            service.get_shopper_email(non_existent_email)
        assert "User not found" in str(exc_info.value.detail)

    def test_update_shopper(self, db: Session):
        """Tests updating a shopper's information"""
        # Arrange
        service = ShopperService(db)
        shopper = ShopperFactory()
        update_data = ShopperUpdate(
            name="Updated Full Name",
            phone_number="555-123-4567",
            email="updated@example.com",
        )

        # Act
        updated_shopper = service.update_shopper(shopper.id, update_data)

        # Assert
        assert updated_shopper.id == shopper.id
        assert updated_shopper.name == "Updated Full Name"
        assert updated_shopper.phone_number == "555-123-4567"
        assert updated_shopper.email == "updated@example.com"

    def test_update_shopper_not_found(self, db: Session):
        """Tests updating a shopper that doesn't exist"""
        # Arrange
        service = ShopperService(db)
        non_existent_id = 2233
        update_data = ShopperUpdate(name="UpdatedFirstName")

        # Act & Assert
        with pytest.raises(NotFound) as exc_info:
            service.update_shopper(non_existent_id, update_data)
        assert "User not found" in str(exc_info.value.detail)

    def test_delete_shopper(self, db: Session):
        """Tests deleting a shopper"""
        # Arrange
        service = ShopperService(db)
        shopper = ShopperFactory()

        # Act
        service.delete_shopper(shopper.id)

        # Assert - should raise NotFound when trying to get the deleted shopper
        with pytest.raises(NotFound):
            service.get_shopper_id(shopper.id)

    def test_delete_shopper_not_found(self, db: Session):
        """Tests deleting a shopper that doesn't exist"""
        # Arrange
        service = ShopperService(db)
        non_existent_id = 2233

        # Act & Assert
        with pytest.raises(NotFound) as exc_info:
            service.delete_shopper(non_existent_id)
        assert "User not found" in str(exc_info.value.detail)
