"""Creating the db engine"""

import os
from typing import Annotated
import logging
import psycopg2
from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

from .user import Shopper, Vendor  # pylint: disable=unused-import

logger = logging.getLogger(__name__)
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DEFAULT_DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
logger.debug("Target database URL: %s", DB_URL)


def ensure_database_exists():
    """Check if database exists, create if not"""
    try:
        # Try connecting to the application database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.close()
        logger.info("Database '%s' already exists", DB_NAME)
    except psycopg2.OperationalError:
        # If we can't connect, the db might not exist, so connect to the default postgres DB
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True  # Need autocommit for CREATE DATABASE
        with conn.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
        conn.close()
        logger.info("Created database '%s'", DB_NAME)


# Create engine after ensuring database exists
engine = create_engine(DB_URL)


def create_db_and_tables():
    """Create all tables defined in SQLModel metadata"""
    ensure_database_exists()
    SQLModel.metadata.create_all(engine)
    logger.info("Tables created successfully")


def get_session():
    """Instantiate the session and yield it as a dependency"""
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_session)]

if __name__ == "__main__":
    create_db_and_tables()
