from typing import Annotated

from fastapi import APIRouter, Path, Body, status

from app.api.dependencies import category_service_dependency
from app.schemas.category import CategorySchema, CategoryUpdateSchema, CategoryCreateSchema

router = APIRouter(prefix="/categories", tags=["category"])


@router.get("", response_model=list[CategorySchema])
def read_categories(service: category_service_dependency) -> list[CategorySchema]:
    return service.read_categories()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
        payload: Annotated[CategoryCreateSchema, Body()],
        service: category_service_dependency
) -> CategorySchema:
    return service.create_category(payload)


@router.patch("/{category_id}")
def update_category(
        category_id: Annotated[str, Path()],
        payload: Annotated[CategoryUpdateSchema, Body()],
        service: category_service_dependency
) -> CategorySchema:
    return service.update_category(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: Annotated[str, Path()], service: category_service_dependency) -> None:
    return service.delete_category(category_id)

