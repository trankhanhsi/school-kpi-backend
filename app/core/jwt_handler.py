from jose import jwt
from datetime import datetime, timedelta

from app.core.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM
)


def create_access_token(user_id: int):

    expire = (
        datetime.utcnow()
        + timedelta(hours=8)
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


def create_refresh_token(user_id: int):

    expire = (
        datetime.utcnow()
        + timedelta(days=30)
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
