from typing import Annotated

from fastapi import APIRouter, Body, Path, status

from app.api.dependencies import task_service_dependency
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema

router = APIRouter(prefix="/tasks", tags=["task"])


@router.get("", response_model=list[TaskSchema])
def read_tasks(service: task_service_dependency) -> list[TaskSchema]:
    return service.read_tasks()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
def create_task(
    payload: Annotated[TaskCreateSchema, Body()], service: task_service_dependency
) -> TaskSchema:
    return service.create_task(payload)


@router.patch("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: Annotated[str, Path()],
    payload: Annotated[TaskUpdateSchema, Body()],
    service: task_service_dependency,
) -> TaskSchema:
    return service.update_task(task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: Annotated[str, Path()], service: task_service_dependency
) -> None:
    return service.delete_task(task_id)
