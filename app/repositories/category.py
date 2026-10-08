from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryModel


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> Sequence[CategoryModel]:
        return self.db.scalars(select(CategoryModel)).all()

    def get_by_id(self, category_id: str) -> CategoryModel | None:
        stmt = select(CategoryModel).where(CategoryModel.id == category_id)
        return self.db.scalars(stmt).first()

    def create(self, name: str) -> CategoryModel:
        category_model = CategoryModel(name=name)

        self.db.add(category_model)
        self.db.flush()

        return category_model

    def delete(self, category_model: CategoryModel) -> None:
        self.db.delete(category_model)
