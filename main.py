from contextlib import asynccontextmanager
from typing import Annotated, Generator
from uuid import uuid4, UUID
from pydantic import BaseModel, ConfigDict

from fastapi import FastAPI, Body, Path, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class TaskModel(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoryModel(Base):
    __tablename__ = "categories"
    name: Mapped[str]


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks", response_model=list[TaskSchema])
def read_tasks(db: Annotated[Session, Depends(get_db)]) -> list[TaskSchema]:
    tasks = db.scalars(select(TaskModel)).all()
    return [TaskSchema.model_validate(task) for task in tasks]


@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
def create_task(payload: Annotated[TaskCreateSchema, Body()], db: Annotated[Session, Depends(get_db)]) -> TaskSchema:
    task_model = TaskModel(title=payload.title)

    db.add(task_model)
    db.commit()

    return TaskSchema.model_validate(task_model)


@app.patch("/tasks/{task_id}", response_model=TaskSchema)
def update_task(
        task_id: Annotated[str, Path()], payload: Annotated[TaskUpdateSchema, Body()],
        db: Annotated[Session, Depends(get_db)]
) -> TaskSchema:
    task_model = db.get(TaskModel, task_id)

    if task_model is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task_model, key, value)

    db.commit()
    return TaskSchema.model_validate(task_model)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: Annotated[str, Path()], db: Annotated[Session, Depends(get_db)]) -> None:
    task_model = db.get(TaskModel, task_id)

    if task_model is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task_model)
    db.commit()


@app.get("/categories", response_model=list[CategorySchema])
def read_categories(db: Annotated[Session, Depends(get_db)]) -> list[CategorySchema]:
    categories = db.scalars(select(CategoryModel)).all()
    return [CategorySchema.model_validate(category) for category in categories]


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(
        payload: Annotated[CategoryCreateSchema, Body()],
        db: Annotated[Session, Depends(get_db)]
) -> CategorySchema:
    category_model = CategoryModel(name=payload.name)

    db.add(category_model)
    db.commit()

    return CategorySchema.model_validate(category_model)


@app.patch("/categories/{category_id}")
def update_category(
        category_id: Annotated[str, Path()],
        payload: Annotated[CategoryUpdateSchema, Body()],
        db: Annotated[Session, Depends(get_db)]
) -> CategorySchema:
    category_model = db.get(CategoryModel, category_id)

    if category_model is None:
        raise HTTPException(status_code=404, detail="Category not found")

    category_model.name = payload.name

    db.commit()
    return CategorySchema.model_validate(category_model)


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: Annotated[str, Path()], db: Annotated[Session, Depends(get_db)]) -> None:
    category_model = db.get(CategoryModel, category_id)

    if category_model is None:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category_model)
    db.commit()
