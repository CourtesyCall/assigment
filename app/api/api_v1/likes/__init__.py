from fastapi import APIRouter

from .view import router as likes_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(likes_router)
