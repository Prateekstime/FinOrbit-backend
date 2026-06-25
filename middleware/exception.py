from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union
from app.utils.logger import logger


async def global_exception_handler(
        request: Request,
        exc: Exception
) -> JSONResponse:
    """
    Global exception handler for all unhandled exceptions
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": str(exc) if exc else None
            }
        }
    )


async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
) -> JSONResponse:
    """
    Handle request validation errors
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(f"Validation error: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": errors
            }
        }
    )


async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
) -> JSONResponse:
    """
    Handle HTTP exceptions
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.detail,
                "message": exc.detail
            }
        }
    )