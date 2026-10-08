import logging
import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routers import router
from app.core.config import settings
from app.core.exceptions import ApiError
from app.core.logging import configure_logging

configure_logging()

app = FastAPI()
logger = logging.getLogger("app.middleware")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    started_at = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as e:
        duration_ms = 1000 * (time.perf_counter() - started_at)
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise e
    duration_ms = 1000 * (time.perf_counter() - started_at)
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


request_number = 0


@app.middleware("http")
async def count_requests(request: Request, call_next) -> Response:
    global request_number

    request_number += 1
    response = await call_next(request)
    response.headers["X-Request-Number"] = str(request_number)

    return response


app.include_router(router)


@app.exception_handler(ApiError)
def api_error_handler(_: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
