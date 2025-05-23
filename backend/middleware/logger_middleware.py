# backend/middleware/logger_middleware.py

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = round(time.time() - start_time, 4)
        method = request.method
        path = request.url.path
        status_code = response.status_code
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "Desconocido")

        logger.info(
            f"[{client_ip}] {method} {path} => {status_code} ({duration}s) | UA: {user_agent}"
        )

        return response
