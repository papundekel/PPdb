from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/persons")

templates = Jinja2Templates(directory="html")


@router.get("/")
async def __get_persons(request: Request):
    return templates.TemplateResponse("persons/index.html.jinja", {"request": request})


@router.get("/create")
async def __create_person(request: Request):
    return templates.TemplateResponse("persons/create.html.jinja", {"request": request})
