import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware

from app.core.rate_limit import limiter
from app.core.settings import settings
from app.routers import api_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    _ = app_
    logger.info('Starting %s %s', settings.app.name, settings.app.version)
    yield
    logger.info('Stopping %s', settings.app.name)


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
    servers=[{'url': server} for server in settings.app.servers],
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
    max_age=settings.cors.max_age,
)

app.include_router(api_router, prefix='/api/v1')


@app.get('/health')
async def health():
    return {'status': 'ok'}
