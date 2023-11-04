from fastapi import APIRouter, Request

from backend.templates import TemplateResponse

router = APIRouter(prefix="/persons")


@router.get("/")
async def get_all(request: Request):
    return TemplateResponse(request, "persons/index")


@router.get("/create")
async def create(request: Request):
    return TemplateResponse(request, "persons/create")
