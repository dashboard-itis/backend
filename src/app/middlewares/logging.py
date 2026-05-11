import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        started_at = time.perf_counter()
        logger.info('Started %s %s', request.method, request.url.path)

        try:
            response = await call_next(request)
        except Exception:
            logger.exception('Failed %s %s', request.method, request.url.path)
            raise

        elapsed_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            'Completed %s %s %s %.2fms',
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response
