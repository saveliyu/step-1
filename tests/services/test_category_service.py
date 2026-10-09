from unittest.mock import Mock

import pytest

from app.core.exceptions import CategoryNotFoundError
from app.models.category import CategoryModel
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryService


class TestReadCategories:
    def test_read_categories_returns_pydantic_models(
        self,
        category_service: CategoryService,
        category_repository_mock: Mock,
    ) -> None:

        category_repository_mock.get_all.return_value = [
            CategoryModel(id="cat-1", name="Books"),
            CategoryModel(id="cat-2", name="Pens"),
        ]

        result = category_service.read_categories()

        assert result == [
            CategorySchema(id="cat-1", name="Books"),
            CategorySchema(id="cat-2", name="Pens"),
        ]

    def test_read_categories_returns_none(
        self,
        category_service: CategoryService,
        category_repository_mock: Mock,
    ) -> None:
        category_repository_mock.get_all.return_value = []

        result = category_service.read_categories()

        assert result == []


#
class TestCreateCategory:
    def test_create_categories_commits(
        self,
        category_service: CategoryService,
        db_mock: Mock,
        category_repository_mock: Mock,
    ) -> None:
        category_repository_mock.create.return_value = CategoryModel(
            id="cat-1", name="Books"
        )

        result = category_service.create_category(CategoryCreateSchema(name="Books"))

        category_repository_mock.create.assert_called_once_with("Books")
        db_mock.commit.assert_called_once_with()

        assert result == CategorySchema(id="cat-1", name="Books")


class TestUpdateCategory:
    def test_update_category_updates(
        self,
        category_service: CategoryService,
        db_mock: Mock,
        category_repository_mock: Mock,
    ) -> None:
        category_repository_mock.get_by_id.return_value = CategoryModel(
            id="cat-1", name="Books"
        )

        result = category_service.update_category(
            "cat-1", CategoryUpdateSchema(name="Pens")
        )

        category_repository_mock.get_by_id.assert_called_once_with("cat-1")
        db_mock.commit.assert_called_once_with()

        assert result == CategorySchema(id="cat-1", name="Pens")

    def test_update_category_raises_when_category_not_found(
        self,
        category_service: CategoryService,
        db_mock: Mock,
        category_repository_mock: Mock,
    ) -> None:
        category_repository_mock.get_by_id.return_value = None

        with pytest.raises(CategoryNotFoundError):
            category_service.update_category("cat-1", CategoryUpdateSchema(name="Pens"))

        db_mock.commit.assert_not_called()
