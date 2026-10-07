from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

book = ""

class BookCreateScheme(BaseModel):
    book: str

@app.post("/book")
async def create_book(payload: Annotated[BookCreateScheme, Body()]) -> None:
    global book
    book = payload.book

@app.get("/book")
async def read_book() -> str:
    global book
    return f"Любимая книга: {book}"