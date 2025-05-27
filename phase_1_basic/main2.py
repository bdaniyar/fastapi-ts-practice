from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

app = FastAPI()

class Products(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(...,max_length=100)
    price: float = Field(..., ge=0.01)
    in_stock: int = Field(...,ge=0)

products_db = {}

@app.get("/")
async def read_root():
    return products_db

@app.get("/products/{product_id}")
async def get_product(product_id: UUID):
    product = products_db.get(product_id)
    if product:
        return {"product_id": product_id, "product": product}
    return {"error": "Продукт не найден"}


@app.post("/products")
async def create_product(product: Products):
    products_db[product.id] = product
    return {"product_id": product.id, "product": product}

@app.put("/products/{product_id}")
async def update_product(product_id: UUID, updated_product: Products):
    if product_id in products_db:
        products_db[product_id] = updated_product
        return {"message": f"Продукт {product_id} обновлён", "product": updated_product}
    return {"error": "Продукт не найден"}

@app.delete("/products/{product_id}")
async def delete_product(product_id: UUID):
    if product_id in products_db:
        del products_db[product_id]
        return {"message":f"Продукт {product_id} удален"}
    return {"error":"Продукт не найден"}
