"""
Main application module for the E-Commerce API
This module initializes the FastAPI application, sets up routers,
and defines the root endpoints.
"""

import logging
from fastapi import FastAPI

from sqlmodel import select

from .core.utils.logger import configure_logging, LogLevels
from .core.db.conn import create_db_and_tables
from .core.db.conn import DbSession
from .core.db.seed import seed_database
from .core.db.user import Shopper, Vendor

logger = logging.getLogger(__name__)
configure_logging(LogLevels.INFO)

app = FastAPI(
    title="E-Commerce API",
    description="Exercise done for Roadmap.sh Python roadmap",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup"""
    logger.info("Initializing database connection")
    create_db_and_tables()

    # Seed the database with default profile
    seed_database()

    logger.info("Database initialization complete")


@app.get("/")
async def root():
    """Root endpoint for the API"""
    return {"message": "Hello World"}


@app.get("/shoppers")
def get_shoppers(db: DbSession):
    """Retrieves all shoppers from the db"""
    shoppers = db.scalars(select(Shopper)).all()
    return shoppers


@app.get("/vendors")
def get_vendors(db: DbSession):
    """Retrieves all vendors from the db"""
    vendors = db.scalars(select(Vendor)).all()
    return vendors
