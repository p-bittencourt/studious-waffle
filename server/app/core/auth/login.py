import logging
import bcrypt
from sqlmodel import Session, select
from app.core.db.user import Shopper, UserLoginFields
from app.core.utils.exceptions import NotFound

logger = logging.getLogger(__name__)


def check_shopper_credentials(db: Session, login_data: UserLoginFields):
    shopper = get_shopper_by_email(db, login_data.email)
    logger.debug(f"Retrieved shopper by email {shopper}")

    password_check = check_password(
        "shopper", login_data.password, shopper.password_hash
    )
    # if password_check:
    # return generate_access_token()

    return {"status": "failure", "message": "Couldn't login user"}


def check_password(submitted_password: str, hashed_password: str) -> bool:
    if bcrypt.checkpw(
        submitted_password.encode("utf-8"), hashed_password.encode("utf-8")
    ):
        return True
    else:
        return False


def get_shopper_by_email(db: Session, user_email: str):
    user = db.scalar(select(Shopper).where(Shopper.email == user_email))
    if not user:
        raise NotFound()
    return user
