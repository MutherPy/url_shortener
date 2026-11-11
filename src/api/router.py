from fastapi import APIRouter
from src.api.create_record import router as create_record_router
from src.api.get_record import router as get_record_router

router = APIRouter()
router.include_router(create_record_router)
router.include_router(get_record_router)

__all__ = ["router"]
