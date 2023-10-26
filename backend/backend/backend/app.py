from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.routers import api, persons

app = FastAPI(redoc_url=None)

app.include_router(persons.router, include_in_schema=False)
app.include_router(api.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
