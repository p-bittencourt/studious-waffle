from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.auth.login import decode_token, get_shopper_by_email
from app.core.db.conn import DbSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(db: DbSession, token: str = Depends(oauth2_scheme)):
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
    except jwt.InvalidTokenError:
        raise credentials_exception
    shopper = get_shopper_by_email(db, user_email)
    return shopper
