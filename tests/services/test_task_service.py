from unittest.mock import Mock

import pytest

from app.core.exceptions import TaskNotFoundError
from app.models.task import TaskModel
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskService


class TestReadTasks:
    def test_read_tasks_returns_pydantic_models(
        self,
        task_service: TaskService,
        task_repository_mock: Mock,
    ) -> None:
        task_repository_mock.get_all.return_value = [
            TaskModel(id="task-1", title="Изучить pytest", completed=False),
            TaskModel(id="task-2", title="Написать первый тест", completed=True),
        ]

        result = task_service.read_tasks()

        assert result == [
            TaskSchema(id="task-1", title="Изучить pytest", completed=False),
            TaskSchema(id="task-2", title="Написать первый тест", completed=True),
        ]

    def test_read_tasks_returns_none(
        self,
        task_service: TaskService,
        task_repository_mock: Mock,
    ) -> None:
        task_repository_mock.get_all.return_value = []

        result = task_service.read_tasks()

        assert result == []


class TestCreateTask:
    def test_create_task_commits(
        self,
        task_service: TaskService,
        db_mock: Mock,
        task_repository_mock: Mock,
    ) -> None:
        created_task = TaskModel(id="task-1", title="task 1", completed=False)
        task_repository_mock.create.return_value = created_task

        result = task_service.create_task(TaskCreateSchema(title="task 1"))

        task_repository_mock.create.assert_called_once_with("task 1")
        db_mock.commit.assert_called_once_with()

        assert result == TaskSchema(id="task-1", title="task 1", completed=False)


class TestUpdateTask:
    @pytest.mark.parametrize(
        ("payload", "expected_title", "expected_completed"),
        [
            pytest.param(
                TaskUpdateSchema(title="task updated", completed=True),
                "task updated",
                True,
            ),
            pytest.param(TaskUpdateSchema(title="task updated"), "task updated", False),
            pytest.param(TaskUpdateSchema(completed=True), "task 1", True),
        ],
    )
    def test_update_task_updates_only_passed_fields(
        self,
        task_service: TaskService,
        db_mock: Mock,
        task_repository_mock: Mock,
        payload: TaskUpdateSchema,
        expected_title: str,
        expected_completed: bool,
    ) -> None:
        task_model = TaskModel(id="task-1", title="task 1", completed=False)
        task_repository_mock.get_by_id.return_value = task_model

        result = task_service.update_task("task-1", payload)

        task_repository_mock.get_by_id.assert_called_once_with("task-1")
        db_mock.commit.assert_called_once_with()

        assert result == TaskSchema(
            id="task-1", title=expected_title, completed=expected_completed
        )

    def test_update_task_raises_when_task_not_found(
        self,
        task_service: TaskService,
        db_mock: Mock,
        task_repository_mock: Mock,
    ) -> None:
        task_repository_mock.get_by_id.return_value = None

        with pytest.raises(TaskNotFoundError):
            task_service.update_task("task-1", TaskUpdateSchema(title="task 1"))

        db_mock.commit.assert_not_called()
