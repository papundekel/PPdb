from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/persons")

templates = Jinja2Templates(directory="html")


@router.get("/")
async def __get_persons(request: Request):
    return templates.TemplateResponse("persons/index.html.jinja", {"request": request})
