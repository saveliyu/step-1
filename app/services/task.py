from sqlalchemy.orm import Session

from app.core.exceptions import TaskNotFoundError
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)

    def read_tasks(self) -> list[TaskSchema]:
        tasks_models = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks_models]

    def create_task(self, payload: TaskCreateSchema) -> TaskSchema:
        task_model = self.task_repository.create(payload.title)
        self.db.commit()
        return TaskSchema.model_validate(task_model)

    def update_task(self, task_id: str, payload: TaskUpdateSchema) -> TaskSchema:
        task_model = self.task_repository.get_by_id(task_id)

        if task_model is None:
            raise TaskNotFoundError

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task_model, key, value)

        self.db.commit()
        return TaskSchema.model_validate(task_model)

    def delete_task(self, task_id: str) -> None:
        task_model = self.task_repository.get_by_id(task_id)

        if task_model is None:
            raise TaskNotFoundError

        self.db.delete(task_model)
        self.db.commit()
        return None
