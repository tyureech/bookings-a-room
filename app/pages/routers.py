import json

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.routers import get_hotels

router = APIRouter(prefix="/page", tags=["Html страницы"])

templates = Jinja2Templates("app/templates")


@router.get("/hotels")
async def get_page_hotels(request: Request, data_hotels: json = Depends(get_hotels)):
    return templates.TemplateResponse(
        "hotels.html", context={"request": request, "hotels": data_hotels}
    )


@router.get("")
async def get_home(request: Request):
    return templates.TemplateResponse("base.html", context={"request": request})
