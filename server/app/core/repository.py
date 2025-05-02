import logging
from typing import List
from sqlmodel import Session, SQLModel, select, update

from app.core.utils.exceptions import BadRequest

logger = logging.getLogger(__name__)


class BaseRepository:

    def get_items(db: Session, model: SQLModel):
        """Retrieves all items from db"""
        return db.scalars(select(model)).all()

    def get_item_id(db: Session, model: SQLModel, item_id: str):
        """Retrieves an item by id"""
        return db.scalar(select(model).where(model.id == item_id))

    def get_item_by_property(
        db: Session, model: SQLModel, db_property: str, item_property: str
    ):
        """Retrevies an item by property"""
        return db.scalar(
            select(model).where(getattr(model, db_property) == item_property)
        )

    def update_item(db: Session, model: SQLModel, item: SQLModel, data: any):
        """Updates an item"""
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_data:
            logger.warning("Couldn't update model #%s", item.id)
            raise BadRequest(detail="No update data provided")

        stmt = (
            update(model)
            .where(getattr(model, "id") == getattr(item, "id"))
            .values(update_data)
        )
        db.exec(stmt)
        db.commit()
        db.refresh(item)

        return item

    def delete_item(db: Session, item: SQLModel):
        """Deletes an item"""
        item_id = getattr(item, "id")
        db.delete(item)
        db.commit()
        logger.info("Deleted item #%s", item_id)
