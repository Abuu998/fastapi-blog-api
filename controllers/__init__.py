from fastapi import APIRouter
from . import posts, users, auth


main_router = APIRouter()


main_router.include_router(auth.router, prefix="/auth")
main_router.include_router(posts.router, prefix="/posts")
main_router.include_router(users.router, prefix="/users")
