from fastapi import Response, Request, HTTPException, Depends, status
from app.config import settings
from app.auth.token_manager import create_access_token, create_refresh_token, verify_token
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from app.database.models import User
from app.database.db import get_db

password_hash = PasswordHash.recommended()

def create_access_refresh_tokens_to_cookie(
        response: Response, 
        sub: int
    ):
    return set_access_refresh_tokens_to_cookie(
        response,
        create_access_token(sub),
        create_refresh_token(sub)
    )
    

def set_access_refresh_tokens_to_cookie(
        response: Response,
        access_token: str, 
        refresh_token: str
    ):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE
    )

    return response

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No token")

    try:
        payload = verify_token(token, "access")
        email = payload.get("sub")
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user

def get_admin_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)

    if (user.role != "ADMIN"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid Role for Request")
    
    return user
