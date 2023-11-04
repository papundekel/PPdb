from fastapi import APIRouter, Request

from backend.templates import TemplateResponse

router = APIRouter(prefix="/users")


@router.get("/login")
async def login(request: Request):
    return TemplateResponse(request, "users/login")


@router.get("/logout")
async def logout(request: Request):
    return TemplateResponse(request, "users/logout")
