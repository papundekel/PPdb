from fastapi import APIRouter

from backend.routers.api import persons

router = APIRouter(prefix="/api")
router.include_router(persons.router)
