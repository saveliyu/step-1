from fastapi import status


class ApiError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Error"


class TaskNotFoundError(ApiError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Task not found"


class CategoryNotFoundError(ApiError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Category not found"
