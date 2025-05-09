"""
Main application module for the E-Commerce API
This module initializes the FastAPI application, sets up routers,
and defines the root endpoints.
"""

import logging
from typing import Annotated
from fastapi import Depends, FastAPI

from fastapi.security import OAuth2PasswordRequestForm

from .core.auth.current_user import ShopperUser
from .core.auth.login import login_for_access_token
from .core.utils.logger import configure_logging, LogLevels
from .core.db.conn import DbSession

from .services.shopper.routes import router as shopper_router
from .services.vendor.routes import router as vendor_router
from .services.product.routes import router as product_router

# from .core.db.conn import create_db_and_tables
from .core.db.seed import seed_database


logger = logging.getLogger(__name__)
configure_logging(LogLevels.DEBUG)

app = FastAPI(
    title="E-Commerce API",
    description="Exercise done for Roadmap.sh Python roadmap",
    version="0.1.0",
)

app.include_router(shopper_router)
app.include_router(vendor_router)
app.include_router(product_router)


def setup_model_relationships():
    """
    This function must be called after all models are imported/defined
    to ensure the SQLModel relationships are properly set up.
    """
    # Import here to avoid circular imports during module loading
    from app.core.db.user import Vendor
    from app.services.product.model import Product

    # At this point, both Product and Vendor classes are fully defined
    # SQLModel will now be able to resolve the relationships

    # You don't need to do anything else here, just importing both
    # models after they're defined is enough


@app.on_event("startup")
async def startup_db_client():
    """Create database and tables on startup"""
    setup_model_relationships()
    # create_db_and_tables()

    # Seed the database with default profile
    seed_database()
    logger.info("Database initialization complete")


@app.get("/")
async def root():
    """Root endpoint for the API"""
    return {"message": "Hello World"}


@app.get("/protected")
def read_protected_items(shopper_user: ShopperUser):
    """Protected endpoint for testing authenticated route"""
    return {"current_user": shopper_user}


@app.post("/login")
def login(db: DbSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Login endpoint"""
    return login_for_access_token(db, form_data)
