from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from redis.asyncio import Redis

from app.core.config import settings
from app.db.session import engine
from app.api.v1.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    description="AI Agent Workflow Orchestration Platform",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(
    tasks_router,
    prefix="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "application": settings.app_name
    }


@app.get("/ready")
async def ready():
    # Check PostgreSQL connectivity.
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    # Check Redis connectivity.
    redis_client = Redis.from_url(
        settings.redis_url,
        decode_responses=True
    )

    try:
        await redis_client.ping()
    finally:
        await redis_client.aclose()

    return {
        "status": "ready",
        "database": "connected",
        "redis": "connected"
    }