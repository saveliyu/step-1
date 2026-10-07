from typing import Annotated
from uuid import uuid4
from pydantic import BaseModel

from fastapi import FastAPI, Body, Path, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str


categories: list[CategorySchema] = []
tasks: list[TaskSchema] = []


@app.get("/tasks")
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: Annotated[TaskCreateSchema, Body()]) -> TaskSchema:
    task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task


@app.patch("/tasks/{id}")
def update_task(id: Annotated[str, Path()], payload: Annotated[TaskUpdateSchema, Body()]) -> TaskSchema:
    for task in tasks:
        if task.id == id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: Annotated[str, Path()]) -> None:
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/categories")
def read_categories() -> list[CategorySchema]:
    return categories


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: Annotated[CategoryCreateSchema, Body()]) -> CategorySchema:
    category = CategorySchema(id=str(uuid4()), name=payload.name)
    categories.append(category)
    return category


@app.patch("/categories/{id}")
def update_category(
        id: Annotated[str, Path()],
        payload: Annotated[CategoryUpdateSchema, Body()]
) -> CategorySchema:
    for category in categories:
        if category.id == id:
            category.name = payload.name
            return category
    raise HTTPException(status_code=404, detail="Category not found")


@app.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: Annotated[str, Path()]) -> None:
    for category in categories:
        if category.id == id:
            categories.remove(category)
            return
    raise HTTPException(status_code=404, detail="Category not found")
