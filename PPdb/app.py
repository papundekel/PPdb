from fastapi import FastAPI

from .routers import persons

app = FastAPI(redoc_url=None)

app.include_router(persons.router)
