from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from fastapi_tasks_db.databasework.hotels.router import get_hotels

router = APIRouter(prefix="/pages", tags=["Фронтенд"])

templates = Jinja2Templates(directory="fastapi_tasks_db/databasework/templates")


@router.get("hotels")
async def get_hotels_page(request: Request, hotels=Depends(get_hotels)):
    return templates.TemplateResponse(
        name="hotels.html", context={"request": request, "hotels": hotels}
    )
