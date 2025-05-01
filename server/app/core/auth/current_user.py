"""
User authentication dependency module.
Provides functionality to extract and validate the current authenticated user from request tokens.
"""

from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.db.conn import DbSession
from app.core.db.user import Shopper, Vendor
from app.core.utils.exceptions import CredentialsException
from .login import decode_token, get_shopper_by_email, get_vendor_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(db: DbSession, token: str = Depends(oauth2_scheme)):
    """
    Extract and validate the current authenticated user from the request token.

    Args:
        db: Database session
        token: JWT token from request authorization header

    Returns:
        Shopper: The authenticated shopper user object
            or
        Vendor: The authenticated vendor user object

    Raises:
        HTTPException: If token is invalid or user cannot be found
    """
    try:
        payload = decode_token(token)
        user_email = payload.get("email")
        if user_email is None:
            raise CredentialsException(detail="Payload didn't contain expected data")
    except jwt.InvalidTokenError as exc:
        raise CredentialsException(detail="Invalid token error") from exc

    shopper = get_shopper_by_email(db, user_email)
    if shopper:
        return shopper

    vendor = get_vendor_by_email(db, user_email)
    if vendor:
        return vendor

    raise CredentialsException(detail="User not found")


ShopperUser = Annotated[Shopper, Depends(get_current_user)]
VendorUser = Annotated[Vendor, Depends(get_current_user)]
