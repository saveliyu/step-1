from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import TaskModel


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> Sequence[TaskModel]:
        return self.db.scalars(select(TaskModel)).all()

    def get_by_id(self, task_id: str) -> TaskModel:
        stmt = select(TaskModel).where(TaskModel.id == task_id)
        task_model = self.db.scalars(stmt).first()

        return task_model

    def create(self, title: str) -> TaskModel:
        task_model = TaskModel(title=title)

        self.db.add(task_model)
        self.db.flush()

        return task_model

    def delete(self, task_model: TaskModel) -> None:
        self.db.delete(task_model)
