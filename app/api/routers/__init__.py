from fastapi import APIRouter

from app.api.routers import category, task

router = APIRouter()

router.include_router(category.router)
router.include_router(task.router)