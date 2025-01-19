from fastapi import APIRouter
from .api_v1.users import router as user_router
from .auth.view import router as auth_router
from .api_v1.comments import router as comment_router
from .api_v1.blogs import router as blogs_router
from .api_v1.category import router as category_router
from .api_v1.likes import router as likes_router

router = APIRouter()

router.include_router(router=auth_router, prefix="/auth")

router.include_router(user_router)
router.include_router(blogs_router)
router.include_router(comment_router)
router.include_router(category_router)
router.include_router(likes_router)
