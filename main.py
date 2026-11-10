from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHttpException


from controllers import main_router

from db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

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
def general_http_exception_handler(exception: StarletteHttpException):
    message = (
        exception.detail 
        if exception.detail 
        else "An error occured, Please check your request and try again."
    )

    return JSONResponse(
        status_code=exception.status_code,
        content={ "detail": message }
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(exception: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={ "detail": exception.errors() }
    )