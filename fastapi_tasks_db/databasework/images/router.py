from fastapi import UploadFile, APIRouter
import shutil

router= APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)

@router.post("/hotels")
async def add_hotel_image(name:int,file:UploadFile):
    with open(f"fastapi_tasks_db/databasework/static/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
