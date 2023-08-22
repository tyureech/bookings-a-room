import aiofiles
from fastapi import APIRouter, UploadFile


router = APIRouter(prefix="/images", tags=["Картинки"])


@router.post("/{id}")
async def add_image(id_image: int, image: UploadFile):
    async with aiofiles.open(f"app/static/images/{id_image}.webp", "wb") as file:
        content = await image.read()
        await file.write(content)
