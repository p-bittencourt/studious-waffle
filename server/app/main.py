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
from .services.order.routes import router as order_router

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
app.include_router(order_router)


def setup_model_relationships():
    """
    This function must be called after all models are imported/defined
    to ensure the SQLModel relationships are properly set up.
    """
    # pylint: disable=import-outside-toplevel,unused-import
    # These imports are intentionally placed here to prevent circular imports
    # and are needed to trigger SQLModel's relationship setup
    from app.core.db.user import Vendor
    from app.core.db.user import Shopper
    from app.services.product.model import Product
    from app.services.order.model import Order, OrderItem

    # pylint: enable=import-outside-toplevel,unused-import


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
