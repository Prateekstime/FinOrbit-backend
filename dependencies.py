from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import jwt

from app.database.database import get_db
from app.config import settings
from app.models.employee import Employee
from app.services.auth_service import AuthService
from app.utils.jwt import decode_token
from app.utils.logger import logger

security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
) -> Employee:
    """
    Get current authenticated user from JWT token
    """
    token = credentials.credentials

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Get user from database
        auth_service = AuthService(db)
        user = await auth_service.get_user_by_id(int(user_id))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_active_user(
        current_user: Employee = Depends(get_current_user)
) -> Employee:
    """
    Get current active user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    return current_user


async def get_current_superuser(
        current_user: Employee = Depends(get_current_active_user)
) -> Employee:
    """
    Get current superuser (admin)
    """
    if current_user.role_id != 1:  # Assuming role_id 1 is admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user


def require_permissions(allowed_roles: list[str]):
    """
    Factory function to create permission dependency
    """

    async def permission_checker(
            current_user: Employee = Depends(get_current_active_user)
    ):
        # Get user role name
        role_name = await AuthService.get_role_name(current_user.role_id)

        if role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {', '.join(allowed_roles)}"
            )
        return current_user

    return permission_checker


async def get_optional_user(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[Employee]:
    """
    Get current user if authenticated, otherwise return None
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials, await get_db())
    except HTTPException:
        return None


async def get_branch_id(
        current_user: Employee = Depends(get_current_active_user)
) -> int:
    """
    Get branch ID from current user
    """
    if not current_user.branch_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no associated branch"
        )
    return current_user.branch_id