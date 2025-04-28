"""
Main application module for the E-Commerce API
This module initializes the FastAPI application, sets up routers,
and defines the root endpoints.
"""

import logging
from typing import Annotated
from fastapi import Depends, FastAPI

from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from .core.auth.current_user import get_current_user
from .core.auth.signup import register_shopper, register_vendor
from .core.auth.login import login_for_access_token
from .core.utils.logger import configure_logging, LogLevels
from .core.db.conn import DbSession
from .core.db.user import (
    Shopper,
    ShopperCreate,
    ShopperPublic,
    Vendor,
    VendorCreate,
    VendorPublic,
)

# from .core.db.conn import create_db_and_tables
# from .core.db.seed import seed_database


logger = logging.getLogger(__name__)
configure_logging(LogLevels.DEBUG)

app = FastAPI(
    title="E-Commerce API",
    description="Exercise done for Roadmap.sh Python roadmap",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_db_client():
    """Create database and tables on startup"""
    # create_db_and_tables()

    # Seed the database with default profile
    # seed_database()
    logger.info("Database initialization complete")


@app.get("/")
async def root():
    """Root endpoint for the API"""
    return {"message": "Hello World"}


@app.get("/protected")
def read_protected_items(current_user: Annotated[str, Depends(get_current_user)]):
    """Protected endpoint for testing authenticated route"""
    return {"current_user": current_user}


@app.post("/login")
def login(db: DbSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Login endpoint"""
    return login_for_access_token(db, form_data)


@app.get("/shoppers", response_model=list[ShopperPublic])
def get_shoppers(db: DbSession):
    """Retrieves all shoppers from the db"""
    shoppers = db.scalars(select(Shopper)).all()
    return shoppers


@app.post("/shoppers")
def add_shopper(db: DbSession, data: ShopperCreate):
    """Adds a Shopper user"""
    return register_shopper(db, data)


@app.get("/vendors", response_model=list[VendorPublic])
def get_vendors(db: DbSession):
    """Retrieves all vendors from the db"""
    vendors = db.scalars(select(Vendor)).all()
    return vendors


@app.post("/vendors")
def add_vendor(db: DbSession, data: VendorCreate):
    """Adds a vendor user"""
    return register_vendor(db, data)
