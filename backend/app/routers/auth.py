from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.auth.token_manager import refresh_access_token
from app.auth.service import create_access_refresh_tokens_to_cookie, set_access_refresh_tokens_to_cookie, get_current_user
from app.schemas.user import UserDto
from app.schemas.auth import LoginUserRequest, RegisterUserRequest
from app.services.user_service import login_user, register_user
from app.database.db import get_db
from sqlalchemy.orm import Session
from app.database.models import User

router = APIRouter()

@router.post("/login", response_model=UserDto)
def login(payload: LoginUserRequest, db: Session = Depends(get_db)):
    try:
        user = login_user(db, payload.email, payload.password)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    dto = UserDto.model_validate(user)

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dto.model_dump()
    )

    return create_access_refresh_tokens_to_cookie(response, user.email)

@router.post("/register", response_model=UserDto)
def register(payload: RegisterUserRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(
            db,
            payload.email,
            payload.login,
            payload.password
        )
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    dto = UserDto.model_validate(user)

    response = JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dto.model_dump()
    )

    return create_access_refresh_tokens_to_cookie(response, user.email)

@router.post("/refresh")
def refresh(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token"
        )
    
    tokens = refresh_access_token(refresh_token)

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token expired or invalid"
        )

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "token refreshed"}
    )

    return set_access_refresh_tokens_to_cookie(
        response, 
        tokens.get("access_token"), 
        tokens.get("refresh_token")
    )

@router.post("/logout")
def logout():
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "logout"}
    )

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response

@router.get("/me", response_model=UserDto)
def me(user: User = Depends(get_current_user)):
    return UserDto.model_validate(user)
