from sqlmodel import SQLModel, create_engine

from user import Shopper, Vendor

DB_URL = ""

engine = create_engine(DB_URL)
SQLModel.metadata.create_all(engine)
