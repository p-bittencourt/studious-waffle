"""Conftest file to setup test db"""

import logging
from typing import Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from app.core.config import Settings

# Import dependencies that need to be overridden
from app.core.db.conn import get_session
from app.main import app
from app.core.db.user import Shopper, Vendor
from app.tests.factories.users import ShopperFactory, VendorFactory

# Set up a test Database
TEST_DB_URI = Settings.TEST_DB_URI
engine = create_engine(TEST_DB_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger(__name__)


def create_test_database():
    """Create the test database if it doesn't exist"""
    db_name = Settings.TEST_DB

    # Create a connection string to the default postgres database
    postgres_uri = f"postgresql://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/postgres"  # pylint: disable=line-too-long

    # Create engine with autocommit=True to allow CREATE DATABASE
    temp_engine = create_engine(postgres_uri, isolation_level="AUTOCOMMIT")

    try:
        # Connect to the postgres database
        with temp_engine.connect() as connection:
            # Check it our test database already exists
            result = connection.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}' ")
            )

            if not result.scalar():
                # Create the test database if it doesn't exist
                logger.info("Creating test database: %s", db_name)
                connection.execute(text(f'CREATE DATABASE "{db_name}"'))
                logger.info("Test database %s created successfully", db_name)
            else:
                logger.info("Test database %s already exists", db_name)
    except Exception as e:
        logger.error("Error creating test database: %s", str(e))
        raise


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """
    create_test_database()
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Create a new database session for each test and roll it back after the test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def set_session_for_factories(db: Session):
    """Attaches the mock session to the factories"""
    ShopperFactory._meta.sqlalchemy_session = db
    VendorFactory._meta.sqlalchemy_session = db


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """Overrides database dependency"""

    def override_get_db():
        yield db

    app.dependency_overrides[get_session] = override_get_db
    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def shopper(db: Session) -> Shopper:
    """Create a test shopper"""
    return ShopperFactory()


@pytest.fixture
def vendor(db: Session) -> Vendor:
    """Create a test vendor"""
    return VendorFactory()
