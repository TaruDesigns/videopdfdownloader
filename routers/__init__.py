from fastapi import APIRouter

from .api import router as apirouter
from .frontend import router as frontrouter

router = APIRouter()

router.include_router(frontrouter, prefix="", tags=["front"])
router.include_router(apirouter, prefix="/api", tags=["api"])
