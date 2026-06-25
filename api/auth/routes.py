from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from typing import Optional

from config import settings
# from schemas.auth import UserLogin, UserRegister, TokenResponse, UserResponse
# from services.auth_service import AuthService
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/login",
             # response_model=TokenResponse
             )
async def login(
        login_data: UserLogin,
        db: AsyncSession = Depends(get_db)
):
    """
    User login endpoint
    """
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": str(user.employee_id), "email": user.email}
    )

    # Create refresh token
    refresh_token = auth_service.create_refresh_token(
        data={"sub": str(user.employee_id)}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/register", response_model=UserResponse)
async def register(
        user_data: UserRegister,
        db: AsyncSession = Depends(get_db)
):
    """
    User registration endpoint
    """
    auth_service = AuthService(db)
    user = await auth_service.register_user(user_data)
    return user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        refresh_token: str,
        db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token
    """
    auth_service = AuthService(db)
    token_data = await auth_service.refresh_access_token(refresh_token)
    return token_data


@router.post("/logout")
async def logout(
        db: AsyncSession = Depends(get_db)
):
    """
    Logout user
    """
    # In a real implementation, you might blacklist the token
    return {"message": "Successfully logged out"}