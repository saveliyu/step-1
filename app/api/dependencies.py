from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.category import CategoryService
from app.services.task import TaskService


def get_task_service(db: Annotated[Session, Depends(get_db)]):
    return TaskService(db)

def get_category_service(db: Annotated[Session, Depends(get_db)]):
    return CategoryService(db)

task_service_dependency = Annotated[TaskService, Depends(get_task_service)]
category_service_dependency = Annotated[CategoryService, Depends(get_category_service)]