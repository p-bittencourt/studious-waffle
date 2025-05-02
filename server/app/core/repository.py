import logging
from typing import List
from sqlmodel import Session, SQLModel, select, update

logger = logging.getLogger(__name__)


class BaseRepository:

    def get_items(db: Session, model: SQLModel):
        """Retrieves all items from db"""
        return db.scalars(select(model)).all()

    def get_item_id(db: Session, model: SQLModel, item_id: str):
        """Retrieves an item by id"""
        return db.scalar(select(model).where(model.id == item_id))
