from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
def read_item(item_id: int, q: str | None = None):
    return {'item_id': item_id, 'q': q}


@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}
