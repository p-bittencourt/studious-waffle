"""
Main application module for the E-Commerce API
This module initializes the FastAPI application, sets up routers,
and defines the root endpoints.
"""

from fastapi import FastAPI
import logging

from .core.utils.logging import configure_logging, LogLevels
from .core.db.conn import create_db_and_tables

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
    logger.info("Database initialization complete")


@app.get("/")
async def root():
    """Root endpoint for the API"""
    return {"message": "Hello World"}
