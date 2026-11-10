from fastapi import FastAPI, status, Request
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHttpException

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


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to SelfBlog"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.exception_handler(StarletteHttpException)
async def general_http_exception_handler(request: Request, exception: StarletteHttpException):
    return await http_exception_handler(request, exception)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    return await request_validation_exception_handler(request, exception)