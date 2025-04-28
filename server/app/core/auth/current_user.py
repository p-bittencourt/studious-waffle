"""
User authentication dependency module.
Provides functionality to extract and validate the current authenticated user from request tokens.
"""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.db.conn import DbSession
from .login import decode_token, get_shopper_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(db: DbSession, token: str = Depends(oauth2_scheme)):
    """
    Extract and validate the current authenticated user from the request token.

    Args:
        db: Database session
        token: JWT token from request authorization header

    Returns:
        Shopper: The authenticated shopper user object

    Raises:
        HTTPException: If token is invalid or user cannot be found
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_email = payload.get("email")
        if user_email is None:
            raise credentials_exception
    except jwt.InvalidTokenError as exc:
        raise credentials_exception from exc
    shopper = get_shopper_by_email(db, user_email)
    return shopper
