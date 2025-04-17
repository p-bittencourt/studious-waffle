"""Creating the db engine"""

import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

from user import Shopper, Vendor

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@" f"{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    """Instantiate the session and yield it as a dependency"""
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_session)]
