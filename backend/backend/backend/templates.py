from fastapi.templating import Jinja2Templates

from backend.users.models import UserDB

templates = Jinja2Templates(directory="html")


def TemplateResponse(request, template_name: str, status_code: int = 200):
    return templates.TemplateResponse(
        f"{template_name}.html.jinja",
        context={"request": request},
        status_code=status_code,
    )
