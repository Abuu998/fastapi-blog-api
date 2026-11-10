from fastapi import APIRouter
from . import posts, users


main_router = APIRouter(
    prefix="/api"
)


main_router.include_router(posts.router)
main_router.include_router(users.router)