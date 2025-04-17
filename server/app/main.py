"""
Main application module for the E-Commerce API
This module initializes the FastAPI application, sets up routers,
and defines the root endpoints.
"""

from fastapi import FastAPI

from .core.utils.logging import configure_logging, LogLevels

configure_logging(LogLevels.INFO)

app = FastAPI(
    title="E-Commerce API",
    description="Exercise done for Roadmap.sh Python roadmap",
    version="0.1.0",
)


@app.get("/")
async def root():
    """Root endpoint for the API"""
    return {"message": "Hello World"}
