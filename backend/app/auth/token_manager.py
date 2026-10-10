import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.config import settings

def create_access_token(sub: int) -> str:
    payload = {
        "sub": str(sub),
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS),
        "iat": datetime.now(timezone.utc)
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(sub: int) -> str:
    payload = {
        "sub": str(sub),
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "iat": datetime.now(timezone.utc)
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str, expected_type: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("type") != expected_type:
            return None

        return payload

    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None

    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def refresh_access_token(refresh_token: str) -> Optional[dict]:
    payload = verify_token(refresh_token, "refresh")

    if not payload:
        return None

    sub = payload["sub"]

    return {
        "access_token": create_access_token(sub),
        "refresh_token": create_refresh_token(sub)
    }
