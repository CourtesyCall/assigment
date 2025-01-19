from fastapi import APIRouter

from .view import router as blogs_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(blogs_router)
