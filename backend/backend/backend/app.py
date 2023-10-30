from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import backend.api as api
import backend.persons.routers.frontend as persons

app = FastAPI(redoc_url=None)

app.include_router(api.router)
app.include_router(persons.router, include_in_schema=False)

app.mount("/static", StaticFiles(directory="static"), name="static")
