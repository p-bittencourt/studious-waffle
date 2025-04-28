"""Manages all environment variables"""

import os
from dotenv import load_dotenv


class Settings:
    """Import all environment variables into the Settings class"""

    load_dotenv()

    ### DATABASE RELATED VARIABLES ###
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    DEFAULT_DB_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
    )

    DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    ### AUTHENTICATION VARIABLES ###
    JWT_SECRET = os.getenv("JWT_SECRET")
