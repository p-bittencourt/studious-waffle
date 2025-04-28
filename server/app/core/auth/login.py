"""
Authentication module for handling user login and token operations.
Provides functions for user authentication, password verification, and JWT token management.
"""

import logging
from typing import Annotated
import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel
from sqlmodel import Session, select
from app.core.db.user import Shopper, Vendor
from app.core.config import Settings
from app.core.utils.exceptions import CredentialsException


logger = logging.getLogger(__name__)


class Token(BaseModel):
    """Define structure of the Token"""

    access_token: str
    token_type: str


def login_for_access_token(
    db: Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Authenticate user and generate access token.

    Args:
        db: Database session
        form_data: Form containing username and password

    Returns:
        Token model with access token and token type

    Raises:
        HTTPException: If authentication fails
    """
    shopper = authenticate_shopper(db, form_data.username, form_data.password)
    vendor = authenticate_vendor(db, form_data.username, form_data.password)
    if not shopper and not vendor:
        raise CredentialsException(
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = generate_access_token(form_data.username)
    return Token(access_token=token, token_type="bearer")


def authenticate_shopper(db: Session, user_email: str, user_password: str) -> bool:
    """
    Verify shopper credentials against stored database values.

    Args:
        db: Database session
        user_email: Email address of the shopper
        user_password: Password submitted by the shopper

    Returns:
        bool: True if authentication succeeds, False otherwise
    """
    shopper = get_shopper_by_email(db, user_email)
    if not shopper:
        return False
    password_check = check_password(user_password, shopper.password_hash)
    if not password_check:
        return False

    return True


def authenticate_vendor(db: Session, user_email: str, user_password: str) -> bool:
    vendor = get_vendor_by_email(db, user_email)
    if not vendor:
        return False
    password_check = check_password(user_password, vendor.password_hash)
    if not password_check:
        return False

    return True


def generate_access_token(email: str):
    """
    Create a JWT token for the authenticated user.

    Args:
        email: User's email to encode in the token

    Returns:
        str: Encoded JWT token
    """
    key = Settings.JWT_SECRET
    encoded = jwt.encode({"email": email}, key, algorithm="HS256")
    return encoded


def decode_token(token):
    """
    Decode a JWT token to extract user information.

    Args:
        token: JWT token string

    Returns:
        dict: Decoded token payload
    """
    key = Settings.JWT_SECRET
    decoded = jwt.decode(token, key, algorithms="HS256")
    return decoded


def check_password(submitted_password: str, hashed_password: str) -> bool:
    """
    Verify if submitted password matches stored hash.

    Args:
        submitted_password: Plain text password submitted by user
        hashed_password: Stored password hash from database

    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        submitted_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_shopper_by_email(db: Session, user_email: str):
    """
    Retrieve shopper record from database by email.

    Args:
        db: Database session
        user_email: Email address to search for

    Returns:
        Shopper: Shopper object if found, None otherwise
    """
    shopper = db.scalar(select(Shopper).where(Shopper.email == user_email))
    return shopper


def get_vendor_by_email(db: Session, user_email: str):
    """
    Retrieve vendor record from database by email.

    Args:
        db: Database session
        user_email: Email address to search for

    Returns:
        Vendor: Vendor object if found, None otherwise
    """
    vendor = db.scalar(select(Vendor).where(Vendor.email == user_email))
    return vendor
