"""Manages all environment variables"""

import os
from dotenv import load_dotenv


class Settings:
    """Import all environment variables into the Settings class"""

    load_dotenv()

    ### DATABASE RELATED VARIABLES ###
    DB_USER = os.getenv("DB_USER") or "postgres"
    DB_PASSWORD = os.getenv("DB_PASSWORD") or "postgres"
    DB_HOST = os.getenv("DB_HOST") or "localhost"
    DB_PORT = os.getenv("DB_PORT") or 5432
    DB_NAME = os.getenv("DB_NAME") or "standard"

    DEFAULT_DB_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
    )

    DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Test DB variables
    TEST_DB = DB_NAME + "_TEST"
    TEST_DB_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@" f"{DB_HOST}:{DB_PORT}/{TEST_DB}"
    )

    ### AUTHENTICATION VARIABLES ###
    JWT_SECRET = os.getenv("JWT_SECRET")
