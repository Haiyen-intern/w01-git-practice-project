from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Book, Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def list_categories(db: Session) -> list[Category]:
    stmt = select(Category).order_by(Category.id)
    return list(db.scalars(stmt).all())

def get_category(db: Session, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def create_category(db: Session, payload: CategoryCreate) -> Category:
    category = Category(name=payload.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(
    db: Session,
    category_id: int,
    payload: CategoryUpdate,
) -> Category:
    category = get_category(db, category_id)
    category.name = payload.name
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = get_category(db, category_id)

    stmt = select(func.count()).select_from(Book).where(Book.category_id == category_id)
    book_count = db.scalar(stmt) or 0

    if book_count > 0:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete category while books exist",
        )
    
    db.delete(category)
    db.commit()