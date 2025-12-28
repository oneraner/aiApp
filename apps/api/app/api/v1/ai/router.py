from fastapi import APIRouter
from . import trigger, stream

router = APIRouter()

router.include_router(trigger.router, prefix="/trigger", tags=["ai"])
router.include_router(stream.router, prefix="/stream", tags=["ai"])
