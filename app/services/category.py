from sqlalchemy.orm import Session

from app.core.exceptions import CategoryNotFoundError
from app.repositories.category import CategoryRepository
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def read_categories(self) -> list[CategorySchema]:
        category_models = self.category_repository.get_all()
        return [CategorySchema.model_validate(category) for category in category_models]

    def create_category(self, payload: CategoryCreateSchema) -> CategorySchema:
        category_model = self.category_repository.create(payload.name)
        self.db.commit()
        return CategorySchema.model_validate(category_model)

    def update_category(
        self, category_id: str, payload: CategoryUpdateSchema
    ) -> CategorySchema:
        category_model = self.category_repository.get_by_id(category_id)

        if category_model is None:
            raise CategoryNotFoundError

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(category_model, key, value)

        self.db.commit()
        return CategorySchema.model_validate(category_model)

    def delete_category(self, category_id: str) -> None:
        category_model = self.category_repository.get_by_id(category_id)

        if category_model is None:
            raise CategoryNotFoundError

        self.db.delete(category_model)
        self.db.commit()
        return None
