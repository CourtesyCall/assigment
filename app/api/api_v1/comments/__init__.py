from fastapi import APIRouter

from .view import router as comment_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(comment_router)
