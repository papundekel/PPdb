from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_200_OK

templates = Jinja2Templates(directory="html")


def TemplateResponse(request, template_name: str, status_code: int = HTTP_200_OK):
    return templates.TemplateResponse(
        f"{template_name}.html.jinja",
        context={"request": request},
        status_code=status_code,
    )
