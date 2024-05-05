from fastapi import APIRouter
from .projects.views import router as projects_router
from .jwt_auth.jwt_auth import router as jwt_router
from app.users.views import router as user_router

router = APIRouter()
# router.include_router(router=jwt_router)
router.include_router(router=user_router, prefix="/users")
router.include_router(router=projects_router, prefix="/projects")
