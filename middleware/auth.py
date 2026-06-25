from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List, Optional
import re

from config import settings
from utils.jwt import decode_token
from utils.logger import logger

EXCLUDED_PATHS = [
    r"^/api/v1/auth/(login|register|refresh|forgot-password|reset-password)",
    r"^/api/v1/health",
    r"^/$",
    r"^/api/docs",
    r"^/api/redoc",
    r"^/api/openapi.json"
]


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for authentication
    """

    async def dispatch(self, request: Request, call_next):
        # Check if path is excluded from authentication
        path = request.url.path

        if self._is_excluded_path(path):
            return await call_next(request)

        # Get authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # Validate token format
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token = auth_header.replace("Bearer ", "")

        try:
            # Validate token
            payload = decode_token(token)
            request.state.user_id = payload.get("sub")
            request.state.user_roles = payload.get("roles", [])
            request.state.token_payload = payload

        except Exception as e:
            logger.warning(f"Authentication failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        response = await call_next(request)
        return response

    def _is_excluded_path(self, path: str) -> bool:
        """
        Check if path is excluded from authentication
        """
        for pattern in EXCLUDED_PATHS:
            if re.match(pattern, path):
                return True
        return False