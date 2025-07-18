import shutil

from fastapi import APIRouter, UploadFile

from fastapi_tasks_db.databasework.tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    with open(
        f"fastapi_tasks_db/databasework/static/images/{name}.webp", "wb+"
    ) as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(f"fastapi_tasks_db/databasework/static/images/{name}.webp")
