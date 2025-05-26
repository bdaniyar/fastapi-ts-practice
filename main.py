from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import uuid4, UUID


app = FastAPI()

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Уникальный идентификатор")
    name: str = Field(..., max_length=50, description="Имя пользователя")
    age: int = Field(..., ge=0, le=120, description="Возраст пользователя")

users_db = {}
user_id_counter = 1

# GET — Получить данные
@app.get("/")
async def read_root():
    return {"message": "Привет, мир!"}

# GET с параметром
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = users_db.get(user_id)
    if user:
        return {"user_id": user_id, "user": user}
    return {"error": "Пользователь не найден"}

# POST — Отправить данные
@app.post("/users")
async def create_user(user: User):
    global user_id_counter
    users_db[user_id_counter] = user
    response = {"user_id": user_id_counter, "user": user}
    user_id_counter += 1
    return response

# PUT — Обновить данные
@app.put("/users/{user_id}")
async def update_user(user_id: int, updated_user: User):
    if user_id in users_db:
        users_db[user_id] = updated_user
        return {"message": f"Пользователь {user_id} обновлён", "user": updated_user}
    return {"error": "Пользователь не найден"}

# DELETE — Удалить пользователя
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id in users_db:
        del users_db[user_id]
        return {"message": f"Пользователь {user_id} удалён"}
    return {"error": "Пользователь не найден"}
