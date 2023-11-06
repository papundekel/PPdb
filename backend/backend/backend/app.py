from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import backend.api as api
import backend.persons.routers.frontend as persons
import backend.profiles.models
import backend.users.routers.frontend as users

app = FastAPI(redoc_url=None)

app.include_router(api.router)
app.include_router(persons.router, include_in_schema=False)
app.include_router(users.router, include_in_schema=False)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse("/static/favicon.ico", 301)
