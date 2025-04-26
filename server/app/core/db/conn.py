"""Creating the db engine"""

from typing import Annotated
import logging
import psycopg2
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

from .user import Shopper, Vendor  # pylint: disable=unused-import
from app.core.config import Settings

logger = logging.getLogger(__name__)


def ensure_database_exists():
    """Check if database exists, create if not"""
    try:
        # Try connecting to the application database
        conn = psycopg2.connect(
            dbname=Settings.DB_NAME,
            user=Settings.DB_USER,
            password=Settings.DB_PASSWORD,
            host=Settings.DB_HOST,
            port=Settings.DB_PORT,
        )
        conn.close()
        logger.info("Database '%s' already exists", Settings.DB_NAME)
    except psycopg2.OperationalError:
        # If we can't connect, the db might not exist, so connect to the default postgres DB
        conn = psycopg2.connect(
            dbname="postgres",
            user=Settings.DB_USER,
            password=Settings.DB_PASSWORD,
            host=Settings.DB_HOST,
            port=Settings.DB_PORT,
        )
        conn.autocommit = True  # Need autocommit for CREATE DATABASE
        with conn.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE "{Settings.DB_NAME}"')
        conn.close()
        logger.info("Created database '%s'", Settings.DB_NAME)


# Create engine after ensuring database exists
engine = create_engine(Settings.DB_URL)


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
