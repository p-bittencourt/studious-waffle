import logging
from typing import Annotated
import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from pydantic import BaseModel
from sqlmodel import Session, select
from app.core.db.user import Shopper
from app.core.config import Settings

logger = logging.getLogger(__name__)


class Token(BaseModel):
    access_token: str
    token_type: str


def login_for_access_token(
    db: Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    shopper = authenticate_shopper(db, form_data.username, form_data.password)
    if not shopper:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = generate_access_token(form_data.username)
    return Token(access_token=token, token_type="bearer")


def authenticate_shopper(db: Session, user_email: str, user_password: str) -> bool:
    shopper = get_shopper_by_email(db, user_email)
    if not shopper:
        return False
    password_check = check_password(user_password, shopper.password_hash)
    if not password_check:
        return False

    return True


def generate_access_token(email: str):
    key = Settings.JWT_SECRET
    encoded = jwt.encode({"email": email}, key, algorithm="HS256")
    return encoded


def decode_token(token):
    key = Settings.JWT_SECRET
    decoded = jwt.decode(token, key, algorithms="HS256")
    return decoded


def check_password(submitted_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        submitted_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_shopper_by_email(db: Session, user_email: str):
    user = db.scalar(select(Shopper).where(Shopper.email == user_email))
    return user
