from fastapi import APIRouter

import backend.persons.routers.api as persons
import backend.users.routers.api as users

router = APIRouter(prefix="/api")
router.include_router(persons.router)
router.include_router(users.router)
