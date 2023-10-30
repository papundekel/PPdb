from fastapi import APIRouter

import backend.persons.routers.api as persons

router = APIRouter(prefix="/api")
router.include_router(persons.router)
