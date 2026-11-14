from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from guard import SecurityConfig, SecurityMiddleware
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHttpException
from config import settings
from contextlib import asynccontextmanager
from controllers import main_router
from db import Base, engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # On Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    # On Shutdown
    await engine.dispose()


config = SecurityConfig(
    enable_rate_limiting=True,
    rate_limit=100,
    rate_limit_window=60,
    enable_penetration_detection=True,
    cors_allow_origins=settings.ORIGIN,
    cors_allow_methods=["*"],
    cors_allow_headers=["*"],
    cors_allow_credentials=True,
    enable_redis=False,
)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=settings.ORIGIN,
)
app.add_middleware(SecurityMiddleware, config=config)

app.include_router(main_router, prefix="/api")


@app.get("/")
def home():
    return {"message": "Welcome to SelfBlog"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.exception_handler(StarletteHttpException)
async def general_http_exception_handler(
    request: Request, exception: StarletteHttpException
):
    return await http_exception_handler(request, exception)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exception: RequestValidationError
):
    return await request_validation_exception_handler(request, exception)
