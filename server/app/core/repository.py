"""
Core repository module providing base database operations.

This module defines the base repository pattern implementation for SQLModel entities.
It provides common CRUD operations and utility methods that can be inherited by
specific repository implementations.
"""

import logging
from typing import List, Any, TypeVar, Type
from sqlmodel import Session, SQLModel, select, update

from app.core.utils.exceptions import BadRequest

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=SQLModel)


class BaseRepository:
    """Base repository class for database operations.

    This class provides common CRUD operations for SQLModel entities.
    """

    def __init__(self, db: Session):
        """Initialize the repository with a database session.

        Args:
            db (Session): SQLModel database session
        """
        self.db = db

    def add_item(self, model: Type[T], model_data: Any) -> T:
        try:
            new_item = model(**model_data.model_dump())
            self.db.add(new_item)
            self.db.commit()
            self.db.refresh(new_item)
            logger.info("Created item")
            return new_item
        except Exception as e:
            logger.error("Failed to add item")
            raise

    def get_items(self, model: Type[T]) -> List[T]:
        """Retrieve all items of the specified model from the database.

        Args:
            model (Type[SQLModel]): The SQLModel class to query

        Returns:
            List[T]: A list of all model instances found in the database
        """
        return self.db.scalars(select(model)).all()

    def get_item_id(self, model: Type[T], item_id: str) -> T:
        """Retrieve a single item by its ID.

        Args:
            model (Type[SQLModel]): The SQLModel class to query
            item_id (str): The ID of the item to retrieve

        Returns:
            T: The model instance if found, otherwise None
        """
        return self.db.scalar(select(model).where(model.id == item_id))

    def get_item_by_property(
        self, model: Type[T], db_property: str, item_property: str
    ) -> T:
        """Retrieve a single item by matching a property value.

        Args:
            model (Type[SQLModel]): The SQLModel class to query
            db_property (str): The model property/column name to filter on
            item_property (str): The value to match against the property

        Returns:
            T: The model instance if found, otherwise None
        """
        return self.db.scalar(
            select(model).where(getattr(model, db_property) == item_property)
        )

    def update_item(self, model: Type[T], item: T, data: Any) -> T:
        """Update an existing item with new data.

        Args:
            model (Type[SQLModel]): The SQLModel class of the item
            item (T): The item instance to update
            data (Any): An object with model_dump method containing update data

        Returns:
            T: The updated model instance

        Raises:
            BadRequest: If no valid update data is provided
        """
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_data:
            logger.warning("Couldn't update model #%s", item.id)
            raise BadRequest(detail="No update data provided")

        stmt = (
            update(model)
            .where(getattr(model, "id") == getattr(item, "id"))
            .values(update_data)
        )
        # Use execute() instead of exec() for better compatibility
        # Some SQLModel/SQLAlchemy versions use exec() while others use execute()
        try:
            # Try the newer exec() method first
            if hasattr(self.db, "exec"):
                self.db.exec(stmt)
            else:
                # Fall back to execute() if exec() is not available
                self.db.execute(stmt)

            self.db.commit()
            self.db.refresh(item)

            return item

        except Exception as e:
            logger.error("Error updating item: %s", str(e))
            raise

    def delete_item(self, item: SQLModel) -> None:
        """Delete an item from the database.

        Args:
            item (SQLModel): The item instance to delete

        Returns:
            None
        """
        item_id = getattr(item, "id")
        self.db.delete(item)
        self.db.commit()
        logger.info("Deleted item #%s", item_id)
