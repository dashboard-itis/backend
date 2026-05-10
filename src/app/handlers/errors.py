import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException

from app.core.exceptions import AppError
from app.schemas.errors import ErrorResponse

logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request,
    exc: AppError,
) -> JSONResponse:
    logger.warning(
        'Application error: %s %s %s',
        request.method,
        request.url.path,
        exc.code,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            code=exc.code,
            message=exc.message,
            details=exc.details,
        ).model_dump(),
    )


async def http_exception_handler(
    _: Request,
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            code='http_error',
            message=str(exc.detail),
        ).model_dump(),
        headers=getattr(exc, 'headers', None),
    )


async def validation_exception_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            code='validation_error',
            message='Validation error',
            details=exc.errors(),
        ).model_dump(),
    )


async def rate_limit_exception_handler(
    _: Request,
    exc: RateLimitExceeded,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=ErrorResponse(
            code='rate_limit_exceeded',
            message=str(exc.detail),
        ).model_dump(),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        'Unhandled error: %s %s',
        request.method,
        request.url.path,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            code='internal_error',
            message='Internal server error',
        ).model_dump(),
    )
